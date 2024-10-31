const database = 'test_db';
const collection = 'companies';

// Create a new database.
use(database);

// Create a new collection.
//db.createCollection(collection);
collection = db.getCollection(collection);
collection.findOne({ticker: 'AAPL'})