-- VietTranslate Database Schema for Supabase PostgreSQL
-- Clean version without RLS triggers

-- 1. Users Table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Translator Profile
CREATE TABLE IF NOT EXISTS translator_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    title VARCHAR(200),
    bio TEXT,
    languages VARCHAR(300),
    badges VARCHAR(200),
    rating FLOAT DEFAULT 0.0,
    total_reviews INTEGER DEFAULT 0,
    total_jobs INTEGER DEFAULT 0,
    response_time VARCHAR(50) DEFAULT '2 giờ',
    is_verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 3. Translator Preference
CREATE TABLE IF NOT EXISTS translator_preference (
    id SERIAL PRIMARY KEY,
    translator_id INTEGER NOT NULL UNIQUE,
    languages TEXT DEFAULT '',
    language_pairs TEXT DEFAULT '',
    FOREIGN KEY (translator_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 4. Service
CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER NOT NULL,
    service_type VARCHAR(50),
    description TEXT,
    language_pair VARCHAR(100),
    price_per_hour INTEGER,
    availability VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES translator_profile(id) ON DELETE CASCADE
);

-- 5. Job
CREATE TABLE IF NOT EXISTS job (
    id SERIAL PRIMARY KEY,
    hirer_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    language_pair VARCHAR(100),
    required_level VARCHAR(50),
    budget DECIMAL(10, 2),
    deadline DATE,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hirer_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 6. Proposal
CREATE TABLE IF NOT EXISTS proposal (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    translator_id INTEGER NOT NULL,
    proposed_price DECIMAL(10, 2),
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE,
    FOREIGN KEY (translator_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 7. Contract
CREATE TABLE IF NOT EXISTS contract (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    translator_id INTEGER NOT NULL,
    hirer_id INTEGER NOT NULL,
    amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE,
    FOREIGN KEY (translator_id) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (hirer_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 8. Message
CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contract(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 9. Direct Message
CREATE TABLE IF NOT EXISTS direct_message (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    content TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 10. Deliverable
CREATE TABLE IF NOT EXISTS deliverable (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER NOT NULL,
    file_url VARCHAR(500),
    submission_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    notes TEXT,
    FOREIGN KEY (contract_id) REFERENCES contract(id) ON DELETE CASCADE
);

-- 11. Review
CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    reviewed_user_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contract(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- 12. Notification
CREATE TABLE IF NOT EXISTS notification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message TEXT,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
CREATE INDEX IF NOT EXISTS idx_job_hirer ON job(hirer_id);
CREATE INDEX IF NOT EXISTS idx_job_status ON job(status);
CREATE INDEX IF NOT EXISTS idx_proposal_job ON proposal(job_id);
CREATE INDEX IF NOT EXISTS idx_proposal_translator ON proposal(translator_id);
CREATE INDEX IF NOT EXISTS idx_contract_job ON contract(job_id);
CREATE INDEX IF NOT EXISTS idx_contract_translator ON contract(translator_id);
CREATE INDEX IF NOT EXISTS idx_contract_hirer ON contract(hirer_id);
CREATE INDEX IF NOT EXISTS idx_direct_message_sender ON direct_message(sender_id);
CREATE INDEX IF NOT EXISTS idx_direct_message_recipient ON direct_message(recipient_id);
CREATE INDEX IF NOT EXISTS idx_notification_user ON notification(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_created ON notification(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_message_contract ON message(contract_id);
CREATE INDEX IF NOT EXISTS idx_deliverable_contract ON deliverable(contract_id);
CREATE INDEX IF NOT EXISTS idx_review_contract ON review(contract_id);
CREATE INDEX IF NOT EXISTS idx_translator_profile_user ON translator_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_translator_preference_user ON translator_preference(translator_id);
CREATE INDEX IF NOT EXISTS idx_service_profile ON service(profile_id);
