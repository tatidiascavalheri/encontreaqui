CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  role VARCHAR(20) NOT NULL CHECK (role IN ('client','professional','advertiser','admin')),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE clients (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT UNIQUE REFERENCES users(id),
  full_name VARCHAR(255),
  location geography(Point,4326)
);

CREATE TABLE categories (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE professionals (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT UNIQUE REFERENCES users(id),
  description TEXT,
  price_cents INT,
  service_radius_km INT DEFAULT 10,
  kyc_status VARCHAR(20) DEFAULT 'pending',
  location geography(Point,4326),
  city VARCHAR(120),
  uf VARCHAR(2)
);

CREATE TABLE professional_categories (
  professional_id BIGINT REFERENCES professionals(id),
  category_id BIGINT REFERENCES categories(id),
  PRIMARY KEY (professional_id, category_id)
);

CREATE TABLE jobs (
  id BIGSERIAL PRIMARY KEY,
  client_id BIGINT REFERENCES clients(id),
  professional_id BIGINT REFERENCES professionals(id),
  category_id BIGINT REFERENCES categories(id),
  status VARCHAR(30) NOT NULL,
  description TEXT,
  scheduled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE job_status_history (
  id BIGSERIAL PRIMARY KEY,
  job_id BIGINT REFERENCES jobs(id),
  old_status VARCHAR(30),
  new_status VARCHAR(30),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE job_attachments (
  id BIGSERIAL PRIMARY KEY,
  job_id BIGINT REFERENCES jobs(id),
  file_url TEXT,
  content_type VARCHAR(80),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE chat_threads (
  id BIGSERIAL PRIMARY KEY,
  job_id BIGINT UNIQUE REFERENCES jobs(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE chat_messages (
  id BIGSERIAL PRIMARY KEY,
  thread_id BIGINT REFERENCES chat_threads(id),
  sender_id BIGINT REFERENCES users(id),
  body TEXT,
  attachment_url TEXT,
  delivered_at TIMESTAMPTZ,
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ratings (
  id BIGSERIAL PRIMARY KEY,
  job_id BIGINT REFERENCES jobs(id),
  rater_id BIGINT REFERENCES users(id),
  target_id BIGINT REFERENCES users(id),
  score INT CHECK (score BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(job_id, rater_id, target_id)
);

CREATE TABLE notifications (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id),
  event_type VARCHAR(80),
  payload JSONB,
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE payments (
  id BIGSERIAL PRIMARY KEY,
  job_id BIGINT UNIQUE REFERENCES jobs(id),
  provider VARCHAR(40),
  provider_payment_id VARCHAR(120),
  amount_cents INT,
  app_fee_cents INT,
  status VARCHAR(30),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE payment_events (
  id BIGSERIAL PRIMARY KEY,
  payment_id BIGINT REFERENCES payments(id),
  event_type VARCHAR(80),
  raw_payload JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE refunds (
  id BIGSERIAL PRIMARY KEY,
  payment_id BIGINT REFERENCES payments(id),
  amount_cents INT,
  reason TEXT,
  status VARCHAR(30),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE payouts (
  id BIGSERIAL PRIMARY KEY,
  payment_id BIGINT REFERENCES payments(id),
  professional_id BIGINT REFERENCES professionals(id),
  amount_cents INT,
  status VARCHAR(30),
  scheduled_at TIMESTAMPTZ,
  paid_at TIMESTAMPTZ
);

CREATE TABLE advertisers (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT UNIQUE REFERENCES users(id),
  company_name VARCHAR(255),
  cnpj VARCHAR(30),
  segment VARCHAR(120)
);

CREATE TABLE campaigns (
  id BIGSERIAL PRIMARY KEY,
  advertiser_id BIGINT REFERENCES advertisers(id),
  name VARCHAR(255),
  billing_model VARCHAR(20) DEFAULT 'CPM',
  budget_cents INT,
  spent_cents INT DEFAULT 0,
  status VARCHAR(20) DEFAULT 'draft',
  starts_at TIMESTAMPTZ,
  ends_at TIMESTAMPTZ
);

CREATE TABLE creatives (
  id BIGSERIAL PRIMARY KEY,
  campaign_id BIGINT REFERENCES campaigns(id),
  image_url TEXT,
  copy TEXT,
  cta TEXT,
  link_url TEXT,
  weight INT DEFAULT 1
);

CREATE TABLE placements (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(40) UNIQUE NOT NULL
);

CREATE TABLE targeting_rules (
  id BIGSERIAL PRIMARY KEY,
  campaign_id BIGINT REFERENCES campaigns(id),
  role VARCHAR(20),
  category_id BIGINT REFERENCES categories(id),
  city VARCHAR(120),
  uf VARCHAR(2),
  center geography(Point,4326),
  radius_km INT
);

CREATE TABLE ad_events (
  id BIGSERIAL PRIMARY KEY,
  campaign_id BIGINT REFERENCES campaigns(id),
  creative_id BIGINT REFERENCES creatives(id),
  event_type VARCHAR(20),
  user_id BIGINT REFERENCES users(id),
  session_id VARCHAR(120),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_prof_location ON professionals USING GIST(location);
CREATE INDEX idx_client_location ON clients USING GIST(location);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_chat_messages_thread_created ON chat_messages(thread_id, created_at DESC);
CREATE INDEX idx_notifications_user_created ON notifications(user_id, created_at DESC);
CREATE INDEX idx_ad_events_campaign_created ON ad_events(campaign_id, created_at DESC);
