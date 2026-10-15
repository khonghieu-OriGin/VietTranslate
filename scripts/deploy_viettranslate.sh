#!/usr/bin/env bash
# ==============================================================================
# Script: deploy_viettranslate.sh
# Purpose: Tự động deploy commit mới nhất từ branch main của GitHub lên VPS
# Tham khảo theo chuẩn CI/CD an toàn cho Linux/Systemd/Nginx:
# 1. Lock file chống xung đột khi có nhiều push cùng lúc (flock)
# 2. Ghi log có mốc thời gian rõ ràng (timestamped logging)
# 3. Git fetch + reset --hard tránh xung đột working tree/cache .pyc
# 4. Bảo toàn tệp môi trường .env, thư mục uploads và storage riêng biệt
# 5. Tự động kiểm tra và cài đặt requirements.txt nếu có thay đổi
# 6. Restart dịch vụ Gunicorn qua Systemd và kiểm tra Health Check (HTTP 200)
# ==============================================================================

set -euo pipefail

# --- CẤU HÌNH THƯ MỤC & DỊCH VỤ ---
PROJECT_DIR="${PROJECT_DIR:-/www/wwwroot/157.66.100.101}"
BRANCH="${DEPLOY_BRANCH:-main}"
SERVICE_NAME="${SERVICE_NAME:-viettranslate.service}"
VENV_DIR="${PROJECT_DIR}/venv"
LOG_FILE="/var/log/viettranslate_deploy.log"
LOCK_FILE="/var/lock/viettranslate_deploy.lock"
APP_USER="www"
APP_GROUP="www"
HEALTH_CHECK_URL="http://127.0.0.1:5000/api/health" # fallback: http://127.0.0.1:5000/

# Đảm bảo thư mục log tồn tại
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
mkdir -p "$(dirname "$LOCK_FILE")" 2>/dev/null || true

log() {
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

log "=========================================================="
log "🚀 [DEPLOY] Bắt đầu quy trình triển khai từ GitHub ($BRANCH)..."

# --- 1. CƠ CHẾ KHÓA ĐỘC QUYỀN (PREVENT CONCURRENT DEPLOYS) ---
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    log "⚠️ [LOCK] Một tiến trình deploy khác đang chạy. Bỏ qua yêu cầu này để tránh xung đột."
    exit 0
fi

# --- 2. KIỂM TRA THƯ MỤC DỰ ÁN ---
if [ ! -d "$PROJECT_DIR/.git" ]; then
    log "❌ [ERROR] Thư mục $PROJECT_DIR không phải là một Git repository hợp lệ."
    exit 1
fi

cd "$PROJECT_DIR"

# Lưu lại commit hash hiện tại trước khi pull
OLD_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
log "ℹ️ [GIT] Commit hiện tại: $OLD_COMMIT"

# --- 3. ĐỒNG BỘ MÃ NGUỒN TỪ GITHUB ---
log "📥 [GIT] Đang fetch mã nguồn mới nhất từ origin/$BRANCH..."
git fetch origin "$BRANCH"

NEW_COMMIT=$(git rev-parse "origin/$BRANCH")
log "ℹ️ [GIT] Commit mới nhất trên origin/$BRANCH: $NEW_COMMIT"

if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
    log "✅ [GIT] Hệ thống đã ở commit mới nhất ($NEW_COMMIT). Không cần cập nhật."
    log "=========================================================="
    exit 0
fi

# Reset --hard để đảm bảo code đồng bộ 100% với commit trên GitHub
# Loại bỏ cache phát sinh hoặc các file untracked không mong muốn (trừ .env, venv, uploads)
log "🔄 [GIT] Đang áp dụng commit mới ($NEW_COMMIT)..."
git reset --hard "origin/$BRANCH"

# Dọn dẹp cache bytecode Python thừa (.pyc) để tránh nạp code cũ
find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# --- 4. CẬP NHẬT DEPENDENCIES NẾU REQUIREMENTS.TXT THAY ĐỔI ---
if git diff --name-only "$OLD_COMMIT" "$NEW_COMMIT" | grep -q "^requirements.txt$"; then
    log "📦 [PIP] Phát hiện thay đổi trong requirements.txt. Đang cập nhật thư viện vào venv..."
    if [ -f "$VENV_DIR/bin/pip" ]; then
        "$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt" --no-cache-dir >> "$LOG_FILE" 2>&1
        log "✅ [PIP] Cập nhật dependencies hoàn tất."
    else
        log "⚠️ [PIP] Không tìm thấy venv tại $VENV_DIR, bỏ qua bước pip install."
    fi
else
    log "ℹ️ [PIP] requirements.txt không thay đổi. Bỏ qua cài đặt thư viện."
fi

# --- 5. ĐỒNG BỘ PHÂN QUYỀN THƯ MỤC CHO USER NGINX/GUNICORN ---
log "🔒 [PERM] Đang phân quyền thư mục cho user $APP_USER:$APP_GROUP..."
chown -R "$APP_USER:$APP_GROUP" "$PROJECT_DIR"
# Đảm bảo file .env chỉ root và www đọc được
if [ -f "$PROJECT_DIR/.env" ]; then
    chmod 600 "$PROJECT_DIR/.env"
fi

# --- 6. KHỞI ĐỘNG LẠI DỊCH VỤ WEB ---
log "🔄 [SERVICE] Đang khởi động lại dịch vụ $SERVICE_NAME..."
if systemctl is-active --quiet "$SERVICE_NAME"; then
    systemctl restart "$SERVICE_NAME"
else
    systemctl start "$SERVICE_NAME"
fi

# Chờ 3 giây để Gunicorn worker khởi động hoàn tất
sleep 3

# --- 7. KIỂM TRA SỨC KHỎE ỨNG DỤNG (HEALTH CHECK) ---
log "🩺 [HEALTH] Đang kiểm tra phản hồi từ ứng dụng..."
HEALTHY=0
for i in {1..5}; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:5000/" || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
        log "✅ [HEALTH] Ứng dụng phản hồi tốt (HTTP $HTTP_CODE) sau lần thử $i."
        HEALTHY=1
        break
    else
        log "⏳ [HEALTH] Thử lần $i: HTTP $HTTP_CODE. Chờ 2s..."
        sleep 2
    fi
done

if [ "$HEALTHY" -eq 1 ]; then
    log "🎉 [SUCCESS] Deploy commit $NEW_COMMIT thành công!"
else
    log "❌ [WARNING] Dịch vụ đã restart nhưng Health Check trả về HTTP $HTTP_CODE. Vui lòng kiểm tra: journalctl -u $SERVICE_NAME -n 50"
fi

log "=========================================================="
exit 0
