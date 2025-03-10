CREATE TABLE IF NOT EXISTS "scheme" (
"id" INTEGER,
  "scheme_name" TEXT,
  "nodal_ministry" TEXT,
  "implementing_agency" TEXT,
  "target_beneficiaries" TEXT,
  "tags" TEXT,
  "state" TEXT,
  "category" TEXT,
  "level" TEXT,
  "brief_description" TEXT,
  "detailed_description" TEXT,
  "eligibility_criteria" TEXT,
  "documents_required" TEXT,
  "application_process" TEXT,
  "benefits" TEXT,
  "Official_Website" TEXT,
  "Application_Form" TEXT,
  "Order/Notice" TEXT,
  "slug" TEXT
);
CREATE INDEX idx_scheme_name ON scheme(scheme_name);
CREATE INDEX idx_scheme_category ON scheme(category);
CREATE INDEX idx_scheme_level ON scheme(level);
CREATE TABLE sqlite_sequence(name,seq);

--- the user should have a column for the kids and their age and other things.

CREATE TABLE user_primary_data (
    user_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    dob DATE NOT NULL,
    sex TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    caste TEXT NOT NULL
);
CREATE INDEX idx_user_id on user_primary_data(user_id);
CREATE INDEX idx_user_phone on user_primary_data(phone_number);
CREATE TABLE user_secondary_data (
    user_id INTEGER NOT NULL,
    address TEXT,
    email TEXT,
    aadhar TEXT,
    PAN TEXT,
    disability TEXT,
    ration_card TEXT,
    marital_status TEXT,
    spouse_details TEXT,
    child_details TEXT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user_primary_data (user_id) ON DELETE CASCADE
);
CREATE INDEX idx_aadhar_card on user_secondary_data(aadhar);
CREATE INDEX idx_pan_card on user_secondary_data(PAN);
CREATE INDEX idx_email_address on user_secondary_data(email);
CREATE TABLE scheme_suggested (
    user_id INTEGER NOT NULL,
    scheme_id INTEGER NOT NULL,
    scheme_name TEXT NOT NULL,
    missing_documents TEXT,
    FOREIGN KEY(user_id) REFERENCES user_primary_data(user_id),
    FOREIGN KEY(scheme_id) REFERENCES scheme(id)
);
CREATE INDEX idx_scheme_suggested_user_id ON scheme_suggested(user_id);
CREATE INDEX idx_scheme_suggested_scheme_id ON scheme_suggested(scheme_id);
CREATE INDEX idx_scheme_suggested_scheme_name ON scheme_suggested(scheme_name);
CREATE TABLE scheme_available (
    user_id INTEGER NOT NULL,
    scheme_id INTEGER NOT NULL,
    scheme_name TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user_primary_data(user_id),
    FOREIGN KEY(scheme_id) REFERENCES scheme(id)
);
CREATE INDEX idx_scheme_avlb_user_id ON scheme_available(user_id);
CREATE INDEX idx_scheme_avlb_scheme_id ON scheme_available(scheme_id);
CREATE INDEX idx_scheme_avlb_scheme_name ON scheme_available(scheme_name);
CREATE TABLE document (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_name TEXT NOT NULL
);
CREATE INDEX idx_document_name ON document(document_name);
CREATE TABLE user_doc (
    user_id INTEGER NOT NULL,
    document_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(user_id),
    FOREIGN KEY(document_id) REFERENCES document(id)
);
CREATE INDEX idx_user_doc_user_id ON user_doc(user_id);
CREATE INDEX idx_user_doc_document_id ON user_doc(document_id);