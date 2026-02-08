const { Pool } = require('pg');

// Load environment variables
require('dotenv').config({path: './.env.local'});

console.log('DATABASE_URL:', process.env.DATABASE_URL); // Debug: log the URL

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { 
    rejectUnauthorized: false 
  },
});

async function testConnection() {
  try {
    console.log('Attempting to connect to database...');
    const result = await pool.query('SELECT NOW()');
    console.log('Database connection successful:', result.rows);
  } catch (err) {
    console.error('Database connection error:', err.message);
    console.error('Error details:', err);
  } finally {
    await pool.end();
  }
}

testConnection();