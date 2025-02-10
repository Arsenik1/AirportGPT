from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class BooleanAgent:
    """
    A boolean verification agent that answers True or False based on the given prompt and data.
    Uses langchain-ollama with qwen2.5:latest.
    """
    def __init__(self, model_name="qwen2.5:latest"):
        """
        Initializes the BooleanAgent with the specified Ollama model.

        Args:
            model_name (str): The name of the Ollama model to use. Defaults to "qwen2.5:latest".
        """
        self.model = ChatOllama(model=model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a boolean verification agent. Your task is to analyze the provided data based on the user's query and respond with ONLY 'True' or 'False'. Do not provide any explanations or other text. Just 'True' or 'False'."),
            ("user", "{query}")
        ])
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.model | self.output_parser

    def run(self, query: str) -> str:
        """
        Executes the boolean verification agent with the given query.

        Args:
            query (str): The user's query describing the verification task and including the data.

        Returns:
            str: "True" or "False" as a string, based on the agent's verification.
        """
        try:
            response = self.chain.invoke({"query": query})
            # Basic cleaning to ensure only "True" or "False" is returned
            cleaned_response = response.strip().lower()
            if cleaned_response == "true":
                return "True"
            elif cleaned_response == "false":
                return "False"
            else:
                # If the model returns something unexpected, default to False or handle as needed
                print(f"Warning: Model returned unexpected boolean response: {response}. Returning 'False' for safety.")
                return "False"
        except Exception as e:
            print(f"Error during agent execution: {e}")
            return "False" # Return False in case of errors

# Example Usage:
if __name__ == '__main__':
    boolean_agent = BooleanAgent()

    # Example 1: Flights present
    json_data_flights = """
    {
      "flights": [
        {"flight_number": "TK123", "departure": "IST", "arrival": "JFK"},
        {"flight_number": "LH456", "departure": "FRA", "arrival": "LAX"}
      ],
      "trains": []
    }
    """
    query_flights = f"Return True if there are any flights in the json data, else return False: {json_data_flights}"
    response_flights = boolean_agent.run(query_flights)
    print(f"Query: {query_flights}\nResponse: {response_flights}")
    assert response_flights == "True"

    # Example 2: No flights present
    json_data_no_flights = """
    {
      "flights": [],
      "trains": [
        {"train_number": "TR789", "departure": "ANK", "arrival": "IST"}
      ]
    }
    """
    query_no_flights = f"Return True if there are any flights in the json data, else return False: {json_data_no_flights}"
    response_no_flights = boolean_agent.run(query_no_flights)
    print(f"Query: {query_no_flights}\nResponse: {response_no_flights}")
    assert response_no_flights == "False"

    # Example 3: Different condition - trains present
    json_data_trains = """
    {
      "flights": [],
      "trains": [
        {"train_number": "TR789", "departure": "ANK", "arrival": "IST"}
      ]
    }
    """
    query_trains = f"Return True if there are any trains in the json data, else return False: {json_data_trains}"
    response_trains = boolean_agent.run(query_trains)
    print(f"Query: {query_trains}\nResponse: {response_trains}")
    assert response_trains == "True"

    # Example 4: No trains present
    json_data_no_trains = """
    {
      "flights": [
        {"flight_number": "TK123", "departure": "IST", "arrival": "JFK"}
      ],
      "trains": []
    }
    """
    query_no_trains = f"Return True if there are any trains in the json data, else return False: {json_data_no_trains}"
    response_no_trains = boolean_agent.run(query_no_trains)
    print(f"Query: {query_no_trains}\nResponse: {response_no_trains}")
    assert response_no_trains == "False"

    # Example 5: More complex JSON and query
    json_data_complex = """
    {
      "travel_options": {
        "flights": [
          {"flight_number": "TK123", "departure": "IST", "arrival": "JFK"},
          {"flight_number": "LH456", "departure": "FRA", "arrival": "LAX"}
        ],
        "trains": []
      },
      "other_info": "some details"
    }
    """
    query_complex_flights = f"Return True if there are any flights under 'travel_options' in the json data, else return False: {json_data_complex}"
    response_complex_flights = boolean_agent.run(query_complex_flights)
    print(f"Query: {query_complex_flights}\nResponse: {response_complex_flights}")
    assert response_complex_flights == "True"

    query_complex_hotels = f"Return True if there are any hotels mentioned in the json data, else return False: {json_data_complex}"
    response_complex_hotels = boolean_agent.run(query_complex_hotels)
    print(f"Query: {query_complex_hotels}\nResponse: {response_complex_hotels}")
    assert response_complex_hotels == "False" # Assuming no hotels in the JSON

    print("All boolean agent examples executed and asserted successfully!")