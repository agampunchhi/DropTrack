
class Item:
    def __init__(self, user, channel, title, price, url, imgURL):
        self.user = user
        self.url = url
        self.title = title
        self.price = price
        self.channel = channel
        self.imgURL = imgURL
        self.id = 0
    