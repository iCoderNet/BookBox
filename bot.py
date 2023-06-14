import sqlite3, os, logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def insert_data(self, table_name, data):
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_data(self, table_name, column_name, new_value, condition):
        query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition}"
        self.cursor.execute(query, (new_value,))
        self.conn.commit()

    def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()
        
    def get_last_element_id(self, table_name):
        query = f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def close(self):
        self.cursor.close()
        self.conn.close()


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu Alaykum. Botga kitobni yuboring men saytga yuklab beraman")



@dp.message_handler(content_types=['document'])
async def echo(message: types.Message):
    doc = message.document
    ex = doc.file_name.split('.')[-1]
    if ex in ['pdf', 'doc', 'docx']:
        d = await doc.download("./media/document/book/")
        db = Database("db.sqlite3")
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(d)
        df = d.name.replace("media", '')
        fn = doc.file_name.replace(ex, '')
        db.insert_data("store_book (name, description, recommended, document, created_at, date, image)", (fn, message.caption, 0, df, formatted_time, 0, 'template.jpg'))
        db.close()
        await message.answer("", reply=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)