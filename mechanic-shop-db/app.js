// 1) load environment variables
require('dotenv').config();

// 2) then use them when you connect to MySQL
const mysql = require('mysql2');
const connection = mysql.createConnection({
  host:     process.env.DB_HOST,
  port:     process.env.DB_PORT,
  user:     process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  charset:  process.env.DB_CHARSET,
  // collation is usually implied by charset
});

connection.connect(err => {
  if (err) {
    console.error('❌ DB connect error:', err);
    process.exit(1);
  }
  console.log('✅ Connected to MySQL!');
});
