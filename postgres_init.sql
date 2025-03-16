CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY,
    user_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    pages_visited TEXT[],
    device TEXT,
    actions TEXT[]
);

CREATE TABLE product_price_history (
    product_id UUID PRIMARY KEY,
    current_price NUMERIC(10, 2),
    currency TEXT
);

CREATE TABLE event_logs (
    event_id UUID PRIMARY KEY,
    timestamp TIMESTAMP,
    event_type TEXT,
    details TEXT
);

CREATE TABLE support_tickets (
    ticket_id UUID PRIMARY KEY,
    user_id INT,
    status TEXT,
    issue_type TEXT,
    messages TEXT[],
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE user_recommendations (
    user_id INT PRIMARY KEY,
    recommended_products UUID[],
    last_updated TIMESTAMP
);

CREATE TABLE moderation_queue (
    review_id UUID PRIMARY KEY,
    user_id INT,
    product_id UUID,
    review_text TEXT,
    rating INT,
    moderation_status TEXT,
    flags TEXT[],
    submitted_at TIMESTAMP
);

CREATE TABLE search_queries (
    query_id UUID PRIMARY KEY,
    user_id INT,
    query_text TEXT,
    timestamp TIMESTAMP,
    filters JSONB,
    results_count INT
);
