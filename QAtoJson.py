import json
import re

def convert_rag_to_json(rag_file_path):
    """
    Converts a text file in RAG Q&A format to JSON.

    Args:
        rag_file_path (str): The path to the rag.txt file.

    Returns:
        str: JSON string representing the Q&A pairs.
    """

    qa_list = []
    current_question = None
    current_answer = ""

    with open(rag_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        if line.startswith(tuple([f"{i+1}. Question:" for i in range(200)])): # Assuming max 200 questions, adjust if needed
            if current_question and current_answer:
                qa_list.append({"question": current_question.strip(), "answer": current_answer.strip()})
                current_answer = ""  # Reset answer for the new question

            current_question = line.split("Question:", 1)[1].strip()


        elif line.startswith("Answer:"):
            # Answer start indicator - no action needed here, answers can span multiple lines
            pass # Answers will be captured in the else condition below

        elif current_question is not None:
             current_answer += line + "\n" # Append lines to the current answer, preserving newlines


    # Add the last Q&A pair if it exists
    if current_question and current_answer:
        qa_list.append({"question": current_question.strip(), "answer": current_answer.strip()})

    return json.dumps({"qa_pairs": qa_list}, indent=4, ensure_ascii=False) # Ensure_ascii=False for unicode chars


if __name__ == "__main__":
    rag_file = "rag.txt"  # Replace with your rag.txt file path
    json_output = convert_rag_to_json(rag_file)
    print(json_output)

    Optional: Save to a JSON file
    with open("qa_output.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_output)
    print(f"JSON output saved to qa_output.json")