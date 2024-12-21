import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from email_utils import EmailSender
from data_loader import DataManager
from config import *

class EmailSenderGUI:
    def __init__(self):
        self.email_sender = EmailSender()
        self.data_manager = DataManager()
        self.recipients = []
        self.attachment_paths = []
        
        self.setup_gui()
        
    def setup_gui(self):
        # Configure theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Main window
        self.window = ctk.CTk()
        self.window.title("Email Sender")
        self.window.geometry("800x600")
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Recipients section
        self.setup_recipients_section()
        
        # Template section
        self.setup_template_section()
        
        # Email content section
        self.setup_email_content_section()
        
        # Attachments section
        self.setup_attachments_section()
        
        # Status section
        self.setup_status_section()
        
        # Set status callback
        self.email_sender.set_status_callback(self.update_status)
        
    def setup_recipients_section(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(frame, text="Recipients").pack(side="left", padx=5)
        
        self.recipient_label = ctk.CTkLabel(frame, text="No recipients loaded")
        self.recipient_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame,
            text="Load CSV",
            command=self.load_recipients
        ).pack(side="right", padx=5)
        
    def setup_template_section(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(frame, text="Template").pack(side="left", padx=5)
        
        self.template_var = ctk.StringVar(value="Select Template")
        self.template_menu = ctk.CTkOptionMenu(
            frame,
            values=self.data_manager.get_template_names(),
            variable=self.template_var,
            command=self.load_template
        )
        self.template_menu.pack(side="left", padx=5)
        
    def setup_email_content_section(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Subject
        subject_frame = ctk.CTkFrame(frame)
        subject_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(subject_frame, text="Subject:").pack(side="left", padx=5)
        self.subject_entry = ctk.CTkEntry(subject_frame)
        self.subject_entry.pack(fill="x", expand=True, padx=5)
        
        # Body
        body_frame = ctk.CTkFrame(frame)
        body_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(body_frame, text="Body:").pack(anchor="w", padx=5)
        self.body_text = ctk.CTkTextbox(body_frame)
        self.body_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def setup_attachments_section(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(frame, text="Attachments:").pack(side="left", padx=5)
        
        self.attachment_label = ctk.CTkLabel(frame, text="No files attached")
        self.attachment_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame,
            text="Add File",
            command=self.add_attachment
        ).pack(side="right", padx=5)
        
    def setup_status_section(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=5, pady=5)
        
        self.status_label = ctk.CTkLabel(frame, text="Ready")
        self.status_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame,
            text="Send Emails",
            command=self.send_emails
        ).pack(side="right", padx=5)
        
    def load_recipients(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                self.recipients = self.data_manager.load_recipients(file_path)
                self.recipient_label.configure(
                    text=f"{len(self.recipients)} recipients loaded"
                )
                self.update_status("Recipients loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def load_template(self, template_name):
        template = self.data_manager.get_template(template_name)
        if template:
            self.subject_entry.delete(0, "end")
            self.subject_entry.insert(0, template["subject"])
            self.body_text.delete("1.0", "end")
            self.body_text.insert("1.0", template["body"])
            
    def add_attachment(self):
        files = filedialog.askopenfilenames()
        if files:
            self.attachment_paths.extend(files)
            self.attachment_label.configure(
                text=f"{len(self.attachment_paths)} files attached"
            )
            
    def update_status(self, message, is_error=False):
        self.status_label.configure(
            text=message,
            text_color="red" if is_error else "white"
        )
        
    def send_emails(self):
        if not self.recipients:
            messagebox.showerror("Error", "No recipients loaded")
            return
            
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", "end")
        
        if not subject or not body.strip():
            messagebox.showerror("Error", "Subject and body are required")
            return
            
        success_count = 0
        for recipient in self.recipients:
            personalized_subject = subject.replace("{name}", recipient["name"])
            personalized_body = body.replace("{name}", recipient["name"])
            
            if self.email_sender.send_email(
                recipient["email"],
                personalized_subject,
                personalized_body,
                self.attachment_paths
            ):
                success_count += 1
                
        messagebox.showinfo(
            "Complete",
            f"Sent {success_count} of {len(self.recipients)} emails successfully"
        )
        
    def run(self):
        self.window.mainloop()