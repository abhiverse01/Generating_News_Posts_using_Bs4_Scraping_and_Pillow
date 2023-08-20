import tkinter as tk
from tkinter import Listbox, PhotoImage, Button, Toplevel, Scrollbar, filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from bs4 import BeautifulSoup
import requests
import logging

# Set up logging
logging.basicConfig(filename="news_post_generator.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def scrape_news(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract headline, sub-text, and date/time
        headline = soup.find('h2').get_text()
        sub_text = soup.find('p').get_text()
        date_time = soup.find('time').get_text()

        return headline, sub_text, date_time
    except Exception as e:
        logging.error(f"Error while scraping news: {e}")
        raise


def show_image(image_path):
    try:
        image_viewer = Toplevel()
        image_viewer.title("Image Viewer")
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(image_viewer, image=photo)
        img_label.image = photo
        img_label.pack()
        back_button = Button(image_viewer, text="Back to List", command=image_viewer.destroy)
        back_button.pack()
    except Exception as e:
        logging.error(f"Error while viewing image: {e}")
        messagebox.showerror("Error", f"An error occurred while viewing the image.")


def load_font(font_path, default_size):
    try:
        return ImageFont.truetype(font_path, default_size)
    except Exception as e:
        logging.error(f"Error while loading font: {e}")
        return ImageFont.load_default()


class NewsPostGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Post Generator")

        self.root.geometry("900x700")  # Adjusted window size

        self.font_headline = load_font("path_to_headline_font.ttf", default_size=24)
        self.font_subtext = load_font("path_to_subtext_font.ttf", default_size=18)

        # Create a translucent background
        self.background = tk.Canvas(root, bg='white', width=900, height=700, highlightthickness=0)
        self.background.pack()
        self.background.place(x=0, y=0)

        # Header
        header_label = tk.Label(root, text="News Post Generator", font=("Helvetica", 20, "bold"))
        header_label.pack(pady=20)

        # Generate Post Button
        self.generate_button = tk.Button(root, text="Generate Post", command=self.generate_post, bg="blue", fg="white",
                                         font=("Helvetica", 12, "bold"))
        self.generate_button.pack()

        # Post History Frame
        history_frame = tk.Frame(root)
        history_frame.pack(pady=20)

        self.history_label = tk.Label(history_frame, text="Post History:", font=("Helvetica", 14))
        self.history_label.pack()

        self.history_listbox = Listbox(history_frame, selectbackground='gray', selectmode=tk.SINGLE, height=8, width=50)
        self.history_listbox.pack(side=tk.LEFT, padx=10)

        self.scrollbar = Scrollbar(history_frame, command=self.history_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=self.scrollbar.set)

        # Bind double click event to view image
        self.history_listbox.bind("<Double-1>", self.view_selected_image)

        self.generated_images = []  # To store generated image paths

        # Footer section
        footer_label = tk.Label(root, text="Developed by: Abhishek Shah | Developed year: 2023 | v 1.0", bg="white")
        footer_label.pack(side=tk.BOTTOM, fill=tk.X)

    def generate_post(self):
        try:
            # Call scraping and image generation functions
            url = 'https://therealnews.com/'
            headline, sub_text, date_time = scrape_news(url)
            image_path = self.generate_social_media_post(headline, sub_text, date_time)
            self.update_history(image_path)  # Change here to update with image_path
            messagebox.showinfo("Success", "Post generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_history(self, image_path):  # Update the method parameter
        self.history_listbox.insert(tk.END, image_path)  # Insert image_path into the listbox


    def generate_social_media_post(self, headline, sub_text, date_time):
        try:
            image = Image.new('RGB', (800, 800), (255, 255, 255, 200))  # Translucent background
            draw = ImageDraw.Draw(image)

            # Draw headline and sub-text
            draw.text((50, 50), headline, fill='black', font=self.font_headline)
            draw.text((50, 150), sub_text, fill='black', font=self.font_subtext)
            draw.text((50, 250), date_time, fill='gray', font=self.font_subtext)

            # Generate a default image name based on serial number
            image_name = f"gen-img[{len(self.generated_images) + 1:02d}].jpg"

            # Show "Save As" dialog to allow the user to choose the file name and location
            image_path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile=image_name,
                                                      filetypes=[("JPEG files", "*.jpg")])

            # Save the image if a file name is provided
            if image_path:
                image.save(image_path)
                self.generated_images.append(image_path)

            return image_path
        except Exception as e:
            logging.error(f"Error while generating image: {e}")
            raise

    def view_selected_image(self, event=None):  # Added event parameter and set default value
        selected_indices = self.history_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]  # Get the first selected index
            selected_image = self.generated_images[selected_index]
            show_image(selected_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = NewsPostGeneratorApp(root)
    root.mainloop()
