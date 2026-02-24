"""Database migration script for renaming user fields and restructuring the schema.

Runs against a production PostgreSQL database serving ~50k daily active users.
"""


def upgrade(connection) -> None:
    """Apply the migration."""
    cursor = connection.cursor()

    # Rename columns in the users table
    cursor.execute("ALTER TABLE users RENAME COLUMN username TO display_name")
    cursor.execute("ALTER TABLE users RENAME COLUMN email_addr TO email")
    cursor.execute("ALTER TABLE users RENAME COLUMN phone_num TO phone")

    # Change column type — widen varchar to text
    cursor.execute("ALTER TABLE users ALTER COLUMN bio TYPE TEXT")

    # Drop the legacy login_count column (no longer tracked)
    cursor.execute("ALTER TABLE users DROP COLUMN login_count")

    # Add new columns
    cursor.execute("ALTER TABLE users ADD COLUMN avatar_url VARCHAR(512)")
    cursor.execute("ALTER TABLE users ADD COLUMN last_active_at TIMESTAMP")

    # Rename the table itself
    cursor.execute("ALTER TABLE user_preferences RENAME TO user_settings")

    # Update a foreign key reference to match the renamed table
    cursor.execute("""
        ALTER TABLE notifications
        DROP CONSTRAINT notifications_user_preferences_fk
    """)
    cursor.execute("""
        ALTER TABLE notifications
        ADD CONSTRAINT notifications_user_settings_fk
        FOREIGN KEY (user_settings_id) REFERENCES user_settings(id)
    """)

    # Rename an index to match the new column name
    cursor.execute("ALTER INDEX idx_users_username RENAME TO idx_users_display_name")

    # Backfill the new last_active_at column from the sessions table
    cursor.execute("""
        UPDATE users u
        SET last_active_at = (
            SELECT MAX(s.created_at)
            FROM sessions s
            WHERE s.user_id = u.id
        )
    """)

    # Drop old views that reference the renamed columns
    cursor.execute("DROP VIEW IF EXISTS active_users_view")
    cursor.execute("DROP VIEW IF EXISTS user_summary_view")

    # Recreate views with new column names
    cursor.execute("""
        CREATE VIEW active_users_view AS
        SELECT id, display_name, email, last_active_at
        FROM users
        WHERE last_active_at > NOW() - INTERVAL '30 days'
    """)

    connection.commit()


def downgrade(connection) -> None:
    """Revert the migration."""
    cursor = connection.cursor()

    cursor.execute("DROP VIEW IF EXISTS active_users_view")

    cursor.execute("ALTER TABLE users RENAME COLUMN display_name TO username")
    cursor.execute("ALTER TABLE users RENAME COLUMN email TO email_addr")
    cursor.execute("ALTER TABLE users RENAME COLUMN phone TO phone_num")

    cursor.execute("ALTER TABLE users DROP COLUMN avatar_url")
    cursor.execute("ALTER TABLE users DROP COLUMN last_active_at")
    cursor.execute("ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0")

    cursor.execute("ALTER TABLE user_settings RENAME TO user_preferences")
    cursor.execute("ALTER INDEX idx_users_display_name RENAME TO idx_users_username")

    connection.commit()
