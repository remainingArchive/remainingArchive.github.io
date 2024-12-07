import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, html_file, monitored_folder):
        self.html_file = html_file
        self.monitored_folder = monitored_folder

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if self.is_image(file_path):
            print(f"New image detected: {file_path}")
            self.add_image_to_html(file_path)
        elif self.is_text(file_path):
            print(f"New text file detected: {file_path}")
            self.add_text_to_html(file_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if self.is_image(file_path):
            print(f"Image deleted: {file_path}")
            self.remove_image_from_html(file_path)
        elif self.is_text(file_path):
            print(f"Text file deleted: {file_path}")
            self.remove_text_from_html(file_path)

    def is_image(self, file_path):
        return any(file_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp'])

    def is_text(self, file_path):
        return file_path.lower().endswith('.txt')

    def add_image_to_html(self, file_path):
        relative_path = os.path.relpath(file_path, os.path.dirname(self.html_file))
        img_tag = f'<img src="{relative_path}" alt="Image">\n'
        print(f"Adding image tag to HTML: {img_tag}")

        with open(self.html_file, 'r') as file:
            content = file.read()

        if '</body>' in content:
            updated_content = content.replace('</body>', f'{img_tag}</body>')
            with open(self.html_file, 'w') as file:
                file.write(updated_content)
            print(f"Updated HTML file: {self.html_file}")
        else:
            print("No </body> tag found in HTML file.")

    def remove_image_from_html(self, file_path):
        relative_path = os.path.relpath(file_path, os.path.dirname(self.html_file))
        img_tag = f'<img src="{relative_path}" alt="Image">\n'
        print(f"Removing image tag from HTML: {img_tag}")

        with open(self.html_file, 'r') as file:
            content = file.read()

        updated_content = content.replace(img_tag, '')
        with open(self.html_file, 'w') as file:
            file.write(updated_content)
        print(f"Updated HTML file: {self.html_file}")

    def add_text_to_html(self, file_path):
        with open(file_path, 'r') as txt_file:
            text_content = txt_file.read()
        p_tag = f'<p>{text_content}</p>\n'
        print(f"Adding text to HTML: {p_tag}")

        with open(self.html_file, 'r') as file:
            content = file.read()

        if '</body>' in content:
            updated_content = content.replace('</body>', f'{p_tag}</body>')
            with open(self.html_file, 'w') as file:
                file.write(updated_content)
            print(f"Updated HTML file: {self.html_file}")
        else:
            print("No </body> tag found in HTML file.")

    def remove_text_from_html(self, file_path):
        with open(file_path, 'r') as txt_file:
            text_content = txt_file.read()
        p_tag = f'<p>{text_content}</p>\n'
        print(f"Removing text from HTML: {p_tag}")

        with open(self.html_file, 'r') as file:
            content = file.read()

        updated_content = content.replace(p_tag, '')
        with open(self.html_file, 'w') as file:
            file.write(updated_content)
        print(f"Updated HTML file: {self.html_file}")

def main():
    monitored_folder = './archive'  # Replace with the path to your folder
    html_file = './index.html'               # Replace with the path to your HTML file

    event_handler = FileHandler(html_file, monitored_folder)
    observer = Observer()
    observer.schedule(event_handler, monitored_folder, recursive=False)
    observer.start()

    print(f'Starting monitoring of folder: {monitored_folder}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
