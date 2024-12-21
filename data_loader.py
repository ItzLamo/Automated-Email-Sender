import pandas as pd
import json
import os

class DataManager:
    def __init__(self):
        self.templates_file = "templates.json"
        self.load_templates()

    def load_recipients(self, file_path):
        """Load recipients from a CSV file"""
        try:
            df = pd.read_csv(file_path)
            required_columns = ['email', 'name']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("CSV must contain 'email' and 'name' columns")
            return df.to_dict(orient='records')
        except Exception as e:
            raise Exception(f"Error loading recipients: {str(e)}")

    def load_templates(self):
        """Load email templates from JSON file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r') as f:
                    self.templates = json.load(f)
            else:
                from config import DEFAULT_TEMPLATES
                self.templates = DEFAULT_TEMPLATES
                self.save_templates()
        except Exception:
            from config import DEFAULT_TEMPLATES
            self.templates = DEFAULT_TEMPLATES

    def save_templates(self):
        """Save email templates to JSON file"""
        try:
            with open(self.templates_file, 'w') as f:
                json.dump(self.templates, f, indent=2)
        except Exception as e:
            print(f"Error saving templates: {str(e)}")

    def add_template(self, name, subject, body):
        """Add or update an email template"""
        self.templates[name] = {
            "subject": subject,
            "body": body
        }
        self.save_templates()

    def get_template(self, name):
        """Get a template by name"""
        return self.templates.get(name, None)

    def get_template_names(self):
        """Get list of template names"""
        return list(self.templates.keys())