import re

def load_auction_item_list(text):
    # Regular expression to match quoted text
    quoted_strings = re.findall(r'"([^"]*)"', text)
    
    return quoted_strings

# Sample input
text = 'LoadAcutionItemList("/Public/Auction/AuctionItems?AuctionId=gjWJkRVw7MeXnwZBuviCYw%3d%3d&Title=klR4M3TcbIzuruVIXCyadw%3d%3d&AuctionTypes=0z4kdQhr4QDyJ%2f43PXsTLQ%3d%3d&image=BbAU1RWYbLmrURpvBpIbYfZQdxXOfdSbbHH1J1bPTreIQ6nB77wUHv%2fPRG5vhRo08TCCeWPl8O5RknWIMv2E%2foPqeVN%2bEhwzhP2BOEfyN2xkwfxGgIRHI92l4aA4dula&totalItems=GchnL2jbCbc0%2bjNRZb3lmw%3d%3d&viewtypeId=KHe6Qcx9tBs9J%2b%2fgnxeL3g%3d%3d&filter=ITUHdU2DoqWvw89vAOs0Dw%3d%3d&pageNumber=pf6Q%2bhJtdeleDd9FfYpy9w%3d%3d")'

# Extract and print the data
extracted_data = load_auction_item_list(text)
print("https://auction.primeauctions.com/" + extracted_data)
print(extracted_data)