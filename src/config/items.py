class Items:
    """User Configuration interface"""
    
    def __init__(self): 
        """Load instance variables"""
        self.category_descriptions = {
            "Food": "Essential products and basic food items that meet your daily nutritional needs, from bread and pasta to dairy products like milk and cheese.",
            "Electronics": "Modern technological devices ranging from smartphones and laptops to televisions and electronic accessories, making everyday life easier with connectivity and entertainment.",
            "Clothing": "Apparel for various occasions, from casual wear like T-shirts and jeans to more sophisticated items like jackets and dresses, ensuring style and comfort.",
            "Books": "A selection of literature for all tastes, from fiction novels to scientific works and biographies, providing knowledge and entertainment.",
            "Furniture": "Essential home furniture, including chairs, tables, and sofas, combining comfort and functionality to improve your living space.",
            "Toys": "Guaranteed fun with toys for all ages, from action figures to puzzles and board games, promoting entertainment and creativity.",
            "Tools": "Practical and essential tools for repairs and DIY projects, like hammers, screwdrivers, and drills, suitable for both small fixes and larger tasks.",
            "Sporting Goods": "Sports equipment for various activities, from footballs to bicycles and tennis rackets, keeping you active and fit.",
            "Automotive": "Essential automotive products to maintain your vehicle’s performance and upkeep, including batteries, tires, oils, and car care accessories.",
            "Health & Beauty": "Personal care and beauty items to take care of your health and appearance, like shampoos, soaps, lotions, and perfumes, keeping you well-groomed.",
            "Home & Garden": "Equipment and supplies to keep your home clean and your garden well-maintained, including vacuum cleaners, lawn mowers, and fertilizers.",
            "Jewelry": "Elegant and sophisticated accessories like necklaces, rings, and watches, adding a touch of luxury and style to your look, perfect for special occasions.",
            "Music": "Musical instruments for music lovers, including guitars, pianos, and violins, allowing you to explore your passion for music and create your own melodies.",
            "Movies": "Films for all tastes and genres, including action, romance, comedy, and horror, providing quality entertainment for your movie nights at home.",
            "Pet Supplies": "Essential products for the care and well-being of your pets, including dog food, cat litter, and accessories for fish and birds.",
            "Software": "Essential programs and applications for your computer, including antivirus software, operating systems, and video and photo editors, ensuring productivity and security.",
            "Video Games": "Electronic games in various genres, such as RPGs, adventure, sports, and racing, offering interactive fun for gamers of all ages and interests."
        }
        self.products_for_categories = {
            "Food": [("Bread", 1.50), ("Rice", 2.00), ("Pasta", 1.75), ("Milk", 1.25), ("Cheese", 3.50)],
            "Electronics": [("Smartphone", 600), ("Laptop", 1200), ("TV", 400), ("Headphones", 80), ("Camera", 500)],
            "Clothing": [("T-shirt", 15), ("Jeans", 40), ("Jacket", 80), ("Dress", 60), ("Shoes", 50)],
            "Books": [("Fiction Novel", 12), ("Science Book", 25), ("Biography", 20), ("Cookbook", 30), ("Dictionary", 35)],
            "Furniture": [("Chair", 75), ("Table", 150), ("Sofa", 500), ("Bed", 800), ("Wardrobe", 400)],
            "Toys": [("Action Figure", 20), ("Doll", 25), ("Board Game", 30), ("Puzzle", 15), ("LEGO", 50)],
            "Tools": [("Hammer", 20), ("Screwdriver", 10), ("Drill", 70), ("Wrench", 15), ("Saw", 25)],
            "Sporting Goods": [("Football", 30), ("Tennis Racket", 100), ("Basketball", 40), ("Bicycle", 300), ("Helmet", 50)],
            "Automotive": [("Car Battery", 150), ("Tire", 100), ("Motor Oil", 30), ("Brake Pad", 60), ("Car Wax", 20)],
            "Health & Beauty": [("Shampoo", 10), ("Soap", 3), ("Toothpaste", 4), ("Lotion", 15), ("Perfume", 50)],
            "Home & Garden": [("Vacuum Cleaner", 200), ("Lawn Mower", 300), ("Garden Hose", 20), ("Light Bulb", 5), ("Fertilizer", 25)],
            "Jewelry": [("Necklace", 150), ("Bracelet", 100), ("Earrings", 75), ("Ring", 200), ("Watch", 250)],
            "Music": [("Guitar", 500), ("Drum Set", 1000), ("Piano", 3000), ("Violin", 800), ("Flute", 400)],
            "Movies": [("Action Movie", 15), ("Romantic Movie", 12), ("Comedy Movie", 10), ("Horror Movie", 14), ("Documentary", 20)],
            "Pet Supplies": [("Dog Food", 30), ("Cat Litter", 15), ("Bird Cage", 50), ("Fish Tank", 100), ("Pet Shampoo", 10)],
            "Software": [("Antivirus", 50), ("Operating System", 100), ("Office Suite", 150), ("Video Editor", 200), ("Photo Editor", 100)],
            "Video Games": [("RPG Game", 60), ("Shooter Game", 60), ("Adventure Game", 50), ("Sports Game", 55), ("Racing Game", 50)]
        }
        self.cargos = {
            "Manager": 5000,
            "Salesperson": 2000,
            "Cashier": 1500,
            "Stock Clerk": 1200,
            "Security Guard": 1000,
            "Intern": 800
        }

