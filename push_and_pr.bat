@echo off
echo ==============================================
echo   Push code module Thu nhap len GitHub
echo ==============================================
git status
git add app.py services/payout_methods.py templates/base.html templates/income_*.html scratch/*.py
git commit -m "feat(income): hoan thien module thu nhap cho phien dich vien (5 muc con)"
git push origin phuonganh/admin
echo Da hoan tat day code len GitHub!
