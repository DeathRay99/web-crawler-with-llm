import json
import requests
from typing import Dict, Optional

class OllamaAnalyzer:
    """Text analyzer using Ollama LLM"""
    
    def __init__(self, model: str = "llama2"):
        self.model = model
        self.base_url = "http://localhost:11434/api"
        
    def analyze_text(self, text: str, title: str = "", url: str = "") -> Dict:
        """Analyze text content and return structured insights"""
        # Truncate text if it's too long
        max_length = 2000
        if len(text) > max_length:
            text = text[:max_length] + "..."
            
        # Create the prompt for the LLM
        prompt = self._create_analysis_prompt(text, title, url)
        
        # Call Ollama API
        response = self._generate_response(prompt)
        
        # Parse the response
        return self._parse_analysis(response)
    
    def _create_analysis_prompt(self, text: str, title: str, url: str) -> str:
        """Create a prompt for the LLM to analyze the text"""
        return f"""
        You are an expert content analyzer. Analyze the following web page content:
        
        URL: {url}
        TITLE: {title}
        
        CONTENT:
        {text}
        
        Please provide the following analysis in JSON format:
        1. A concise summary (max 150 words)
        2. The main category this content belongs to (choose one: technology, business, health, politics, science, entertainment, sports, education, finance, cybersecurity, other)
        3. The overall sentiment (positive, neutral, negative)
        4. Three key insights or recommendations based on this content
        
        Return ONLY valid JSON with these fields: summary (string), category (string), sentiment(string), insights (array of strings)

        Example output:
       {
        "summary": "Crawl4AI Documentation provides information on setting up and using the Crawl4AI platform for web crawling, including installation, quick start, blog, and advanced features.",
        "category": "technology",
        "sentiment": "neutral",
        "insights": [
            "The documentation provides a comprehensive overview of the platform's features and capabilities.",
            "The blog section offers valuable insights and updates on the latest developments in web crawling technology.",
            "The quick start guide is a useful resource for those looking to get started with Crawl4AI quickly."
        ]
       }
        """
    
    def _generate_response(self, prompt: str) -> str:
        """Make an API call to Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()

            print("\n--- RAW LLM RESPONSE ---")
            print(response.json().get("response", ""))
            print("--- END OF RESPONSE ---\n")

            return response.json().get("response", "")
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error calling Ollama API: {e}")
            return ""
    
    def _parse_analysis(self, response: str) -> Dict:
        """Parse the LLM response into structured data"""
        try:
            # Try to extract JSON from the response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            
            # If no valid JSON is found, create a simplified structure
            return {
                "summary": self._extract_section(response, "summary"),
                "category": self._extract_section(response, "category"),
                "sentiment": self._extract_section(response, "sentiment"),
                "insights": self._extract_insights(response)
            }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "summary": "Error analyzing content",
                "category": "other",
                "sentiment": "neutral",
                "insights": ["Analysis failed"]
            }
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from text"""
        lines = text.splitlines()
        capture = False
        result = []

        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()

            if lower.startswith(section_name.lower()):
                parts = stripped.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip()  # Inline value found
                capture = True
                continue

            if capture:
                # If we hit a new section, stop capturing
                if any(lower.startswith(header) for header in ["category", "sentiment", "insight"]):
                    break
                if stripped:
                    result.append(stripped)

        return " ".join(result).strip()

    
    def _extract_insights(self, text: str) -> list:
        """Extract insights from text response"""
        insights = []
        if "insight" in text.lower() or "recommendation" in text.lower():
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if line and (line.startswith("- ") or line.startswith("* ") or 
                            any(line.lower().startswith(f"{i}.") for i in range(1, 10))):
                    insights.append(line.lstrip("- *123456789. "))
        
        # If no insights found, try to split by numbers
        if not insights and "insight" in text.lower():
            sections = text.lower().split("insight")
            if len(sections) > 1:
                for section in sections[1:]:
                    insights.append(section.strip()[:100])
        
        return insights[:3]  # Limit to 3 insights
    

# if __name__ == "__main__":
#     # Instantiate the analyzer
#     analyzer = OllamaAnalyzer(model="llama2")

#     # Sample input text
#     sample_text = """
#     Apple Inc. has announced the launch of its latest iPhone 15 model, featuring a new titanium body,
#     enhanced camera system, and improved battery life. The tech giant claims this will be the most powerful iPhone yet.
#     The event also highlighted Apple's continued commitment to sustainability and carbon neutrality.
#     """

#     # Run analysis
#     result = analyzer.analyze_text(
#         text=sample_text,
#         title="Apple Launches iPhone 15",
#         url="https://example.com/apple-iphone15"
#     )

#     # Pretty print result
#     print(json.dumps(result, indent=2))
