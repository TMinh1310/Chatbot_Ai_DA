import pymysql
import openai
import os
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

class ActionFetchInformation(Action):
    def name(self) -> Text:
        return "action_fetch_information"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        connection = None
        try:
            # Kết nối tới cơ sở dữ liệu
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="1234",
                database="rasa",
                cursorclass=pymysql.cursors.DictCursor
            )

            # Lấy thông tin từ slot
            query = tracker.get_slot("subtopic")
            if not query:
                dispatcher.utter_message("Please specify a valid topic or subtopic you want to know about.")
                return []

            # Debugging: Log thông tin đầu vào
            print(f"User asked about: {query}")

            # Truy vấn cơ sở dữ liệu
            with connection.cursor() as cursor:
                sql = """
                    SELECT 
                        c.name AS chapter_name, 
                        t.name AS topic_name, 
                        s.name AS subtopic_name,
                        IFNULL(d.description, '') AS detail_description, 
                        IFNULL(d.conditions, '') AS conditions, 
                        IFNULL(d.characteristics, '') AS characteristics,
                        IFNULL(e.example_description, '') AS example_description, 
                        IFNULL(e.application, '') AS application
                    FROM chapter c
                    LEFT JOIN topics t ON c.chapter_id = t.chapter_id
                    LEFT JOIN subtopics s ON t.topic_id = s.topic_id
                    LEFT JOIN details d ON s.subtopic_id = d.subtopic_id
                    LEFT JOIN examples e ON d.detail_id = e.detail_id
                    WHERE c.name LIKE %s OR t.name LIKE %s OR s.name LIKE %s
                """

                # Log câu truy vấn SQL
                print(f"Executing SQL: {sql}")

                cursor.execute(sql, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
                results = cursor.fetchall()

                # Xử lý kết quả
                if results:
                    response = self.format_response(results)
                    dispatcher.utter_message(response)
                else:
                    dispatcher.utter_message(f"Sorry, I couldn't find any information about '{query}'.")

            # Thêm thông tin từ OpenAI nếu cần
            self.ask_openai(query, dispatcher)

        except pymysql.MySQLError as e:
            # Ghi log lỗi MySQL
            print(f"MySQL Error: {e.args[0]} - {e.args[1]}")
            dispatcher.utter_message(f"An error occurred while querying the database: {str(e)}")
        except Exception as e:
            # Ghi log lỗi bất ngờ
            print(f"Unexpected Error: {e}")
            dispatcher.utter_message(f"An unexpected error occurred: {str(e)}")
        finally:
            if connection:
                connection.close()
                print("Database connection closed.")

        return []

    def format_response(self, results: List[Dict[Text, Any]]) -> str:
        """
        Format lại phản hồi dựa trên kết quả truy vấn.
        """
        response = ""
        for row in results:
            if row.get("chapter_name"):
                response += f"**Chapter:** {row['chapter_name']}\n"
            if row.get("topic_name"):
                response += f"**Topic:** {row['topic_name']}\n"
            if row.get("subtopic_name"):
                response += f"**Subtopic:** {row['subtopic_name']}\n"
            if row.get("detail_description"):
                response += f"**Details:** {row['detail_description']}\n"
            if row.get("conditions"):
                response += f"**Conditions:** {row['conditions']}\n"
            if row.get("characteristics"):
                response += f"**Characteristics:** {row['characteristics']}\n"
            if row.get("example_description"):
                response += f"**Example:** {row['example_description']} (Application: {row['application']})\n"
            response += "\n"
        return response.strip()

    def ask_openai(self, query: str, dispatcher: CollectingDispatcher):
        """
        Lấy thêm thông tin từ OpenAI nếu cần.
        """
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not openai_api_key:
            dispatcher.utter_message("OpenAI API key is not set. Please configure it to enable this feature.")
            return

        openai.api_key = openai_api_key

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Provide detailed technical information about: {query}.",
                max_tokens=200
            )
            openai_response = response.choices[0].text.strip()
            if openai_response:
                dispatcher.utter_message(f"Here's some additional information from OpenAI:\n{openai_response}")
            else:
                dispatcher.utter_message("I couldn't retrieve additional information from OpenAI at the moment.")
        except Exception as e:
            dispatcher.utter_message(f"An error occurred while fetching data from OpenAI: {str(e)}")
