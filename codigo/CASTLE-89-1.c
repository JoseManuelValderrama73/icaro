// create table existential_crises (id INT, name VARCHAR(12))
// insert into existential_crises values (1, "abc")

#include <stdio.h>
#include <sqlite3.h>

int main() {
    sqlite3 *db;
    sqlite3_stmt *res;
    int rc;

    rc = sqlite3_open("crises.db", &db);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    // Prepare an SQL query
    char id[32];
    printf("Enter the id of the record: ");
    fgets(id, sizeof(id), stdin);
    char sql[256];
    snprintf(sql, sizeof(sql), "SELECT * FROM existential_crises WHERE id = '%s'", id);

    // Compile the SQL query
    rc = sqlite3_prepare_v2(db, sql, -1, &res, 0);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    // Execute SQL query
    while (sqlite3_step(res) == SQLITE_ROW) {
        int id = sqlite3_column_int(res, 0);
        const unsigned char *name = sqlite3_column_text(res, 1);

        printf("ID: %d | Name: %s\n", id, name);
    }

    // Finalize and clean up
    sqlite3_finalize(res);
    sqlite3_close(db);

    return 0;
}