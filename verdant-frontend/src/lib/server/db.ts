import pkg from 'pg';

const { Pool } = pkg;

export const db = new Pool({
    host: 'localhost',
    port: 5432,
    user: 'postgres',
    password: 'postgres',
    database: 'verdant_hvac'
});