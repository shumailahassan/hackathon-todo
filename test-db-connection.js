// Simple test to check database connectivity
import { Pool } from 'pg';

async function testConnection() {
  const connectionString = process.env.DATABASE_URL;
  
  if (!connectionString) {
    console.error('DATABASE_URL is not set in environment variables');
    return;
  }

  const pool = new Pool({
    connectionString: connectionString,
    ssl: {
      rejectUnauthorized: false, // For Neon databases
    },
  });

  try {
    console.log('Attempting to connect to the database...');
    const client = await pool.connect();
    console.log('Connected successfully!');
    
    // Test a simple query
    const result = await client.query('SELECT NOW()');
    console.log('Query result:', result.rows[0]);
    
    client.release();
  } catch (err) {
    console.error('Connection failed:', err);
  } finally {
    await pool.end();
  }
}

testConnection();