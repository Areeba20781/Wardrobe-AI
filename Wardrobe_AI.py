import requests
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# WeatherService class: Responsible for fetching weather data
class WeatherService:
    """Encapsulation: Handles fetching weather data."""
    @staticmethod
    def get_weather(location):
        """Fetches weather information for the given location using OpenWeatherMap API."""
        api_key = "26142b0c32098c1ecaf1972fb76cea78"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        try:
            # Sending GET request to the weather API
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:  # If API response is successful
                # Extracting required weather details
                main = data["main"]
                weather = data["weather"][0]["main"]
                description = data["weather"][0]["description"]
                temperature = main["temp"]
                humidity = main["humidity"]
                wind_speed = data["wind"]["speed"]
                return weather.lower(), temperature, description, humidity, wind_speed
            else:
                return None, None, None, None, None
        except Exception as e:
            # Error handling if API call fails
            print(f"Error fetching weather data: {e}")
            return None, None, None, None, None

# RecommendationService class: Extends WeatherService to provide clothing recommendations
class RecommendationService(WeatherService):
    """Inheritance: Extends WeatherService to provide recommendations."""
    @staticmethod
    def get_recommendation(gender, style, weather, event):
        """Generates clothing recommendations based on user preferences and weather."""
        # Validate event and style compatibility
        if (style == "sporty" and event == "wedding") or (style == "formal" and event == "gym"):
            return "No recommendations available for this combination.", None

        # Outfit recommendations for different weather and user preferences
        recommendations = {
             "boy": {
                "casual": {"rain": ("Rain jacket, sneakers", "https://cache4.pakwheels.com/ad_pictures/1042/rain-suit-and-rain-shoes-waterproof-shoes-cover-with-rain-suit-waterproof-raincoat-with-hood-1-1-pair-104273038.webp"), "clear": ("T-shirt, shorts", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6Zj3SNQe-rtCcwiupAWZipAtgO2rBk3enww&s"), "cold": ("Sweater, jeans", "https://www.acecart.pk/cdn/shop/files/39-1_0b5a1400-35d1-4f26-8f57-9034c8c9c6b7.webp?v=1730928801&width=1200")},
                "formal": {"rain": ("Waterproof blazer, formal shoes", "https://backend.daman.co.id/wp-content/uploads/2012/10/73150360_02-73268254_OA-73350250_RE.jpg"), "clear": ("Formal shirt, trousers", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHvwzJ8ig6CxmBMGTTplBz6qTphONSpw_s6Q&s"), "cold": ("Suit, overcoat", "https://d1fufvy4xao6k9.cloudfront.net/looks/1024/grey-long-overcoat-charcoal-grey-shawl-suit-1.jpg")},
                "sporty": {"rain": ("Waterproof tracksuit", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRO1yJ08Ch46HV4tG0-KxjSntmeuxvD_0OfgQ&s"), "clear": ("Sports T-shirt, shorts", "https://teetall.pk/cdn/shop/products/coordsettt3.png?v=1678894996"), "cold": ("Hoodie, joggers", "https://thehawk.pk/cdn/shop/files/7_75be7f58-14c9-4d9e-81bd-e1dcc86d359e.jpg?v=1699947586")},
            },
            "girl": {
                "casual": {"rain": ("Raincoat, boots", "https://i.pinimg.com/736x/79/25/f7/7925f733f798b0708db8251e269a443e.jpg"), "clear": ("Summer dress, sandals", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4B3Y_HkhhskO_QFzgJ_GDdda_dtgBb07ujA&s"), "cold": ("Cozy sweater, leggings", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc6pp8za9MGSgT6CE6EFoSsoznoQGbZu7wUQ&s")},
                "formal": {"rain": ("Elegant raincoat, boots", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxacXKbnE-SYdkmjyk8oUtxO775VnqP_8ckQ&s"), "clear": ("Formal blouse, skirt", "https://img.ltwebstatic.com/images3_pi/2023/01/16/167386115551bb5a3ef3c7b3fa646cff38b15ddbee_thumbnail_720x.jpg"), "cold": ("Formal coat, scarf", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1V9jb15mxsmuAXVArxOcxtduGzTwdf4REow&s")},
                "sporty": {"rain": ("Waterproof activewear", "https://images2.drct2u.com/plp_full_width_1/products/mr/mr327/z01mr327705w.jpg"), "clear": ("Sports tracksuit, trouser", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYPE6f8pJanA7Gb_8MHbciL_jGQlnmKDatgQ&s"), "cold": ("Tracksuit", "https://ausman.pk/cdn/shop/files/ladies-tracksuit-in-pakistan.webp?v=1694668344&width=1100")},
            },
        }

        # Special events (wedding, gym) override default recommendations
        if event == "wedding":
            if gender == "boy":
                return "Formal suit with tie", "https://i.ytimg.com/vi/I2PELmvJSFM/maxresdefault.jpg"
            elif gender == "girl":
                return "Elegant gown with accessories", "https://cdn0.weddingwire.in/article/8417/original/1280/jpg/107148-wedding-dresses-for-girls-9.jpeg"
        elif event == "gym":
            if gender == "boy":
                return "Activewear and running shoes", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLiPCNxABDJ6GVdek6tyJiqEqJY0tGD7tcYQ&s"
            elif gender == "girl":
                return "Sports bra and leggings", "https://image.clovia.com/media/images/categorybannergeneric/gym-wear-Mob-Category_6878666.jpg"

        # General weather-based recommendations
        weather_key = "rain" if "rain" in weather else "clear" if "clear" in weather else "cold"
        return recommendations[gender][style][weather_key]

# Main GUI Application
class WardrobeAIApp:
    def __init__(self, root):
        """Initializes the application GUI."""
        self.root = root
        self.root.title("Wardrobe AI")
        self.root.geometry("500x700")  # Adjusted window size
        self.root.resizable(True, True)  # Enable resizing
        self.root.configure(bg="#f0f4f8")  # Set default background

        self.previous_weather = None  # Tracks previously fetched weather
        self.theme = "light"  # Default theme
        self.create_widgets()  # Calls method to create UI elements

    def compare_weather(self, new_weather):
        """Compares current weather with previously fetched weather."""
        if not self.previous_weather:
            return "No previous weather data to compare."

        comparison = []
        if new_weather[1] > self.previous_weather[1]:
            comparison.append("It's warmer today.")
        elif new_weather[1] < self.previous_weather[1]:
            comparison.append("It's colder today.")
        else:
            comparison.append("The temperature is the same as before.")

        return " ".join(comparison)

    def toggle_theme(self):
        """Toggles between light and dark themes."""
        if self.theme == "light":
            self.root.configure(bg="#2d2d2d")
            self.theme = "dark"
            fg_color = "#ffffff"
            bg_color = "#2d2d2d"
        else:
            self.root.configure(bg="#f0f4f8")
            self.theme = "light"
            fg_color = "#495057"
            bg_color = "#f0f4f8"

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.configure(bg=bg_color, fg=fg_color)

    def create_widgets(self):
        """Creates and lays out the application's GUI widgets."""
        # Header Section
        header_frame = tk.Frame(self.root, bg="#41167c")
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(
            header_frame, text="Wardrobe AI", font=("Helvetica", 20, "bold"), bg="#41167c", fg="white"
        )
        header_label.pack(pady=10)

        # Theme Toggle Button
        theme_button = tk.Button(
            header_frame, text="Toggle Theme", font=("Arial", 10), bg="#ffffff", fg="#41167c", command=self.toggle_theme
        )
        theme_button.pack(side=tk.RIGHT, padx=5)

        # Input Section: Name, Location, Gender, Style, Event
        input_frame = tk.Frame(self.root, bg="#f0f4f8")
        input_frame.pack(pady=10)

        # Name Input
        tk.Label(input_frame, text="What is your name?", font=("Arial", 12), bg="#f0f4f8").grid(row=0, column=0, pady=5, sticky="w")
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25, bg="#e9ecef", fg="#495057")
        self.name_entry.grid(row=0, column=1, padx=5)

        # Location Input
        tk.Label(input_frame, text="What is your location?", font=("Arial", 12), bg="#f0f4f8").grid(row=1, column=0, pady=5, sticky="w")
        self.location_entry = tk.Entry(input_frame, font=("Arial", 12), width=25, bg="#e9ecef", fg="#495057")
        self.location_entry.grid(row=1, column=1, padx=5)

        # Gender Selection
        tk.Label(input_frame, text="Recommendation for:", font=("Arial", 12), bg="#f0f4f8").grid(row=2, column=0, pady=5, sticky="w")
        self.gender_var = tk.StringVar()
        gender_frame = tk.Frame(input_frame, bg="#f0f4f8")
        gender_frame.grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(gender_frame, text="Boy", variable=self.gender_var, value="boy").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Girl", variable=self.gender_var, value="girl").pack(side=tk.LEFT, padx=5)

        # Style Selection
        tk.Label(input_frame, text="Choose your style preferences:", font=("Arial", 12), bg="#f0f4f8").grid(row=3, column=0, pady=5, sticky="w")
        self.style_var = tk.StringVar()
        style_frame = tk.Frame(input_frame, bg="#f0f4f8")
        style_frame.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(style_frame, text="Casual", variable=self.style_var, value="casual").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(style_frame, text="Formal", variable=self.style_var, value="formal").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(style_frame, text="Sporty", variable=self.style_var, value="sporty").pack(side=tk.LEFT, padx=5)

        # Event Selection
        tk.Label(input_frame, text="What's the occasion?", font=("Arial", 12), bg="#f0f4f8").grid(row=4, column=0, pady=5, sticky="w")
        self.event_var = tk.StringVar()
        event_frame = tk.Frame(input_frame, bg="#f0f4f8")
        event_frame.grid(row=4, column=1, sticky="w")
        ttk.Radiobutton(event_frame, text="None", variable=self.event_var, value="none").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(event_frame, text="Wedding", variable=self.event_var, value="wedding").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(event_frame, text="Gym", variable=self.event_var, value="gym").pack(side=tk.LEFT, padx=5)

        # Recommendation Button
        recommend_button = tk.Button(
            self.root, text="Get Recommendation", font=("Arial", 14), bg="#41167c", fg="white", command=self.show_recommendation
        )
        recommend_button.pack(pady=20)

        # Result Section
        result_frame = tk.Frame(self.root, bg="#f0f4f8", bd=2, relief=tk.GROOVE)
        result_frame.pack(pady=10, fill=tk.X, padx=10)
        self.result_label = tk.Label(result_frame, text="", font=("Arial", 12), bg="#f0f4f8", wraplength=450, fg="#495057")
        self.result_label.pack(pady=10)
        self.link_button = tk.Button(result_frame, text="View Outfit", font=("Arial", 12), fg="#41167c", cursor="hand2", bg="#f0f4f8")

        # Footer Section
        footer_label = tk.Label(
            self.root, text="Powered by Wardrobe AI © 2025", font=("Arial", 10), bg="#f0f4f8", fg="#6c757d"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def show_recommendation(self):
        """Generates and displays the clothing recommendation."""
        # Collect user inputs
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()
        style = self.style_var.get()
        gender = self.gender_var.get()
        event = self.event_var.get()

        # Input validation
        if not name:
            messagebox.showerror("Input Error", "Please enter your name.")
            return
        if not location:
            messagebox.showerror("Input Error", "Please enter your location.")
            return
        if not style:
            messagebox.showerror("Input Error", "Please select your style preference.")
            return
        if not gender:
            messagebox.showerror("Input Error", "Please select whether it's for a boy or girl.")
            return

        # Fetch weather data
        weather, temperature, description, humidity, wind_speed = RecommendationService.get_weather(location)
        if weather is None:
            messagebox.showerror("Weather Error", "Unable to fetch weather data. Please check your location spelling.")
            return

        # Fetch recommendations
        recommendation, link = RecommendationService.get_recommendation(gender, style, weather, event)

        if link is None:
            self.result_label.config(text=f"Hi {name}, {recommendation}")
            self.link_button.pack_forget()
        else:
            weather_comparison = self.compare_weather((weather, temperature))
            self.previous_weather = (weather, temperature)

            # Display recommendation details
            self.result_label.config(
                text=(f"Hi {name}, based on the weather in {location}:\n\n"
                      f"Recommended Outfit: {recommendation}\n"
                      f"Temperature: {temperature}°C\n"
                      f"Weather: {description}\n"
                      f"Humidity: {humidity}%\n"
                      f"Wind Speed: {wind_speed} m/s\n\n"
                      f"Weather Comparison: {weather_comparison}")
            )
            # Add link button to open outfit link
            self.link_button.config(text="View Outfit", command=lambda: webbrowser.open(link))
            self.link_button.pack()

# Main block to start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WardrobeAIApp(root)
    root.mainloop()
