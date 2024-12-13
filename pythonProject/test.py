import requests
import pandas as pd
import time
import re

# Chatbot API endpoint
CHATBOT_API = "http://localhost:5005/webhooks/rest/webhook"

# Dữ liệu kiểm tra
test_cases = [
    {"test_id": 1, "question": "What is the structure of a MOSFET?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 2, "question": "Define threshold voltage in MOS transistors.", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 3, "question": "Explain the I-V characteristics of MOSFET.", "expected_subtopic": "I-V Characteristics"},
    {"test_id": 4, "question": "What is the cutoff mode in MOS operation?", "expected_subtopic": "Cutoff Mode"},
    {"test_id": 5, "question": "Describe triode mode in MOSFET.", "expected_subtopic": "Triode Mode"},
    {"test_id": 6, "question": "When does a MOSFET operate in saturation?", "expected_subtopic": "Saturation Mode"},
    {"test_id": 7, "question": "How does a common source amplifier work?", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 8, "question": "What is the purpose of a source follower?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 9, "question": "What are small-signal parameters in MOSFET?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 10, "question": "Define the small-signal equivalent circuit.", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 11, "question": "What are the terminals of a MOS transistor?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 12, "question": "How is threshold voltage affected by doping?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 13, "question": "Explain the linear region of MOS operation.", "expected_subtopic": "Triode Mode"},
    {"test_id": 14, "question": "Describe the conditions for cutoff mode.", "expected_subtopic": "Cutoff Mode"},
    {"test_id": 15, "question": "What is the gain of a common source amplifier?", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 16, "question": "When is a source follower used?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 17, "question": "What is transconductance in MOSFET?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 18, "question": "What defines the bandwidth of a circuit?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 19, "question": "Provide an example of MOSFET in cutoff mode.", "expected_subtopic": "Cutoff Mode"},
    {"test_id": 20, "question": "Give an example of MOSFET in triode mode.", "expected_subtopic": "Triode Mode"},
    {"test_id": 21, "question": "What is the role of saturation in amplification?", "expected_subtopic": "Saturation Mode"},
    {"test_id": 22, "question": "Explain the role of gate capacitance in MOS.", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 23, "question": "What does Vth represent in MOSFET?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 24, "question": "Why is the saturation region useful?", "expected_subtopic": "Saturation Mode"},
    {"test_id": 25, "question": "How is a common source amplifier designed?", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 26, "question": "What is the ideal gain of a source follower?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 27, "question": "How is output resistance calculated?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 28, "question": "What components are in a small-signal circuit?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 29, "question": "Define a MOS transistor's body terminal.", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 30, "question": "What factors influence threshold voltage?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 31, "question": "Explain the triode region formula.", "expected_subtopic": "Triode Mode"},
    {"test_id": 32, "question": "What is the small-signal gain of a MOSFET?", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 33, "question": "Why use a source follower in circuits?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 34, "question": "What is the formula for transconductance?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 35, "question": "What is the purpose of small-signal models?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 36, "question": "Provide an example of MOSFET amplification.", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 37, "question": "What are the operating regions of MOSFET?", "expected_subtopic": "I-V Characteristics"},
    {"test_id": 38, "question": "How does doping affect threshold voltage?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 39, "question": "What is the importance of gate capacitance?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 40, "question": "Describe the high-gain mode of MOSFET.", "expected_subtopic": "Saturation Mode"},
    {"test_id": 41, "question": "What is a MOS transistor's inversion layer?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 42, "question": "Explain MOSFET as a voltage buffer.", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 43, "question": "How to calculate g_m in small-signal models?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 44, "question": "What are key components in small-signal circuits?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 45, "question": "When is triode mode used in MOSFET?", "expected_subtopic": "Triode Mode"},
    {"test_id": 46, "question": "What is the current equation in saturation mode?", "expected_subtopic": "Saturation Mode"},
    {"test_id": 47, "question": "Define the voltage gain of common-source amps.", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 48, "question": "Describe the linear operation of MOSFET.", "expected_subtopic": "Triode Mode"},
    {"test_id": 49, "question": "Why use MOSFET in high-frequency circuits?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 50, "question": "What is the effect of V_{GS} on MOS?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 51, "question": "What are the basic building blocks of analog circuits?", "expected_subtopic": "Introduction to Analog CMOS"},
    {"test_id": 52, "question": "Describe the structure of a MOS transistor.", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 53, "question": "How does doping affect the threshold voltage of a MOSFET?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 54, "question": "What is the significance of the oxide layer in MOS transistors?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 55, "question": "Explain the I-V characteristics of a MOSFET.", "expected_subtopic": "I-V Characteristics"},
    {"test_id": 56, "question": "When does a MOSFET operate in cutoff mode?", "expected_subtopic": "Cutoff Mode"},
    {"test_id": 57, "question": "What is the current equation for triode mode operation?", "expected_subtopic": "Triode Mode"},
    {"test_id": 58, "question": "Describe the conditions required for saturation mode.", "expected_subtopic": "Saturation Mode"},
    {"test_id": 59, "question": "What is the role of the common source amplifier in analog circuits?", "expected_subtopic": "MOSFET as Common Source Amplifier"},
    {"test_id": 60, "question": "Explain the concept of a source follower.", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 61, "question": "How is transconductance (g_m) calculated in MOSFETs?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 62, "question": "What components are included in the small-signal equivalent circuit?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 63, "question": "What are the common applications of current mirrors?", "expected_subtopic": "Current Mirrors"},
    {"test_id": 64, "question": "How does an operational amplifier differ from a MOS amplifier?", "expected_subtopic": "Operational Amplifiers"},
    {"test_id": 65, "question": "What factors influence the frequency response of amplifiers?", "expected_subtopic": "Frequency Response"},
    {"test_id": 66, "question": "Explain the role of differential amplifiers in noise reduction.", "expected_subtopic": "Differential Amplifiers"},
    {"test_id": 67, "question": "What are the major noise sources in MOSFETs?", "expected_subtopic": "Noise in MOSFETs"},
    {"test_id": 68, "question": "How does body effect influence the operation of a MOSFET?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 69, "question": "Explain the concept of channel length modulation.", "expected_subtopic": "I-V Characteristics"},
    {"test_id": 70, "question": "What is the relationship between V_{GS} and I_{D} in triode mode?", "expected_subtopic": "Triode Mode"},
    {"test_id": 71, "question": "What is the advantage of using a source follower in load driving?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 72, "question": "How does a small-signal model aid in circuit analysis?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 73, "question": "Why is the cutoff region important in digital circuits?", "expected_subtopic": "Cutoff Mode"},
    {"test_id": 74, "question": "Describe an example of MOSFET operation in saturation mode.", "expected_subtopic": "Saturation Mode"},
    {"test_id": 75, "question": "What is the purpose of current mirrors in analog design?", "expected_subtopic": "Current Mirrors"},
    {"test_id": 76, "question": "What determines the gain of a differential amplifier?", "expected_subtopic": "Differential Amplifiers"},
    {"test_id": 77, "question": "Explain the role of common-mode rejection in differential amplifiers.", "expected_subtopic": "Differential Amplifiers"},
    {"test_id": 78, "question": "How is thermal noise minimized in MOSFET circuits?", "expected_subtopic": "Noise in MOSFETs"},
    {"test_id": 79, "question": "What defines the small-signal gain of an amplifier?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 80, "question": "What are the operating regions of a MOSFET?", "expected_subtopic": "I-V Characteristics"},
    {"test_id": 81, "question": "How does an operational amplifier achieve high gain?", "expected_subtopic": "Operational Amplifiers"},
    {"test_id": 82, "question": "What are the limitations of MOSFETs in high-frequency applications?", "expected_subtopic": "Frequency Response"},
    {"test_id": 83, "question": "Explain the impact of V_{DS} on MOSFET performance.", "expected_subtopic": "Saturation Mode"},
    {"test_id": 84, "question": "What is the purpose of using a small-signal equivalent model?", "expected_subtopic": "Small-Signal Equivalent Circuit"},
    {"test_id": 85, "question": "How is gate capacitance modeled in MOSFET analysis?", "expected_subtopic": "Structure and Symbols"},
    {"test_id": 86, "question": "What are the differences between NMOS and PMOS devices?", "expected_subtopic": "MOS Fundamentals"},
    {"test_id": 87, "question": "What is the formula for drain current in triode mode?", "expected_subtopic": "Triode Mode"},
    {"test_id": 88, "question": "How is noise modeled in small-signal MOSFET circuits?", "expected_subtopic": "Noise in MOSFETs"},
    {"test_id": 89, "question": "What is the effect of substrate doping on V_{th}?", "expected_subtopic": "Threshold Voltage (Vth)"},
    {"test_id": 90, "question": "What factors influence the stability of frequency response?", "expected_subtopic": "Frequency Response"},
    {"test_id": 91, "question": "Explain the concept of feedback in operational amplifiers.", "expected_subtopic": "Operational Amplifiers"},
    {"test_id": 92, "question": "How does load impedance affect the performance of a source follower?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 93, "question": "What is the purpose of common-mode rejection ratio (CMRR)?", "expected_subtopic": "Differential Amplifiers"},
    {"test_id": 94, "question": "Explain the significance of noise figure in analog circuits.", "expected_subtopic": "Noise in MOSFETs"},
    {"test_id": 95, "question": "What is the ideal gain of a source follower?", "expected_subtopic": "MOSFET as Source Follower"},
    {"test_id": 96, "question": "What is the role of drain-source resistance in MOSFET operation?", "expected_subtopic": "I-V Characteristics"},
    {"test_id": 97, "question": "Explain the role of capacitance in frequency response analysis.", "expected_subtopic": "Frequency Response"},
    {"test_id": 98, "question": "How is r_o calculated in small-signal models?", "expected_subtopic": "Small-Signal Parameters"},
    {"test_id": 99, "question": "What is the use of voltage gain in operational amplifiers?", "expected_subtopic": "Operational Amplifiers"},
    {"test_id": 100, "question": "How do differential amplifiers enhance signal integrity?", "expected_subtopic": "Differential Amplifiers"},
]



# Lưu kết quả
results = []

# Hàm gửi câu hỏi và nhận phản hồi
def send_question(question):
    response = requests.post(
        CHATBOT_API,
        json={"sender": "test_user", "message": question},
        timeout=5
    )
    return response.json()

# Hàm trích xuất subtopic từ phản hồi của bot
def extract_subtopic(bot_reply):
    match = re.search(r"\*\*Subtopic:\*\* (.+)", bot_reply)
    if match:
        return match.group(1).strip()
    return "Unknown"

# Chạy kiểm tra
for case in test_cases:
    test_id = case["test_id"]
    question = case["question"]
    expected_subtopic = case["expected_subtopic"]

    start_time = time.time()
    try:
        response = send_question(question)
        end_time = time.time()

        bot_reply = response[0].get("text", "") if response else "No response"
        detected_subtopic = extract_subtopic(bot_reply)

        is_correct = detected_subtopic == expected_subtopic

        results.append({
            "Test Case ID": test_id,
            "Input (Question)": question,
            "Expected Subtopic": expected_subtopic,
            "Detected Subtopic": detected_subtopic,
            "Correct": "Yes" if is_correct else "No",
            "Response Time (ms)": round((end_time - start_time) * 1000, 2),
            "Bot Reply": bot_reply,
            "Comment": "" if is_correct else "Detected wrong subtopic."
        })

    except Exception as e:
        results.append({
            "Test Case ID": test_id,
            "Input (Question)": question,
            "Expected Subtopic": expected_subtopic,
            "Detected Subtopic": "Error",
            "Correct": "No",
            "Response Time (ms)": "N/A",
            "Bot Reply": str(e),
            "Comment": "Error occurred."
        })

# Chuyển kết quả thành DataFrame chính
df_main = pd.DataFrame(results)

# Bảng 2: Phân tích theo subtopic
subtopic_analysis = df_main.groupby("Expected Subtopic").agg(
    Total_Test_Cases=("Test Case ID", "count"),
    Correct_Cases=("Correct", lambda x: sum(x == "Yes")),
    Incorrect_Cases=("Correct", lambda x: sum(x == "No"))
)
subtopic_analysis["Accuracy (%)"] = round(
    (subtopic_analysis["Correct_Cases"] / subtopic_analysis["Total_Test_Cases"]) * 100, 2
)

# Bảng 3: Thời gian phản hồi
response_time_analysis = df_main[["Test Case ID", "Expected Subtopic", "Response Time (ms)"]].copy()
response_time_analysis.rename(columns={"Expected Subtopic": "Subtopic"}, inplace=True)
response_time_analysis["Comment"] = response_time_analysis["Response Time (ms)"].apply(
    lambda x: "Fast" if x <= 200 else "Moderate" if x <= 500 else "Slow"
)

# Bảng 4: Tổng hợp hiệu suất
total_test_cases = len(df_main)
correct_cases = sum(df_main["Correct"] == "Yes")
average_response_time = round(df_main["Response Time (ms)"].mean(), 2)
overall_performance = pd.DataFrame([
    {"Metric": "Total Test Cases", "Value": total_test_cases},
    {"Metric": "Correctly Identified (%)", "Value": round((correct_cases / total_test_cases) * 100, 2)},
    {"Metric": "Average Response Time", "Value": f"{average_response_time} ms"}
])

# Xuất kết quả ra file Excel
output_file = "chatbot_test_results.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df_main.to_excel(writer, sheet_name="Overview", index=False)
    subtopic_analysis.to_excel(writer, sheet_name="Subtopic Analysis")
    response_time_analysis.to_excel(writer, sheet_name="Response Time Analysis", index=False)
    overall_performance.to_excel(writer, sheet_name="Performance Summary", index=False)

print(f"Test results saved to {output_file}")
