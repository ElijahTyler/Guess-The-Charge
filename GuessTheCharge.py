import re
import random
import requests
from bs4 import BeautifulSoup

def main():
    def compile():
        charges = []
        mugshots = []
        valid_list = soup.find_all('div', attrs={"class": "charge-title",})

        for charge in valid_list:
            # Remove tags from charge
            charge_str = f'{charge}'
            tags_to_remove = re.findall("<.*?>", charge_str)
            for tag in tags_to_remove:
                charge_str = charge_str.replace(tag, ' ') if tag == '\n' else charge_str.replace(tag, '')
            
            if '#1' in charge_str:
                charges.append(charge_str[3:])

                # Navigate backwards through the tree to find the photo, and append to mugshots
                new_space = charge.parent.parent.parent.parent.previous_sibling.previous_sibling.a.span
                mugshot = new_space['data-large']
                mugshots.append(mugshot)

        return charges, mugshots
    
    def get_info(charges, mugshots):
        print(charges, f'\n\n{len(charges)}\n\n', mugshots, f'\n\n{len(mugshots)}\n\n')
        return

    random_page = random.randint(3, 20)
    r = requests.get(f'https://michigan.arrests.org/?page={random_page}&results=28')
    soup = BeautifulSoup(r.text, 'html.parser')

    charges, mugshots = compile()
    get_info(charges, mugshots)

    unlucky_number = random.randint(0, len(charges)-1) # chooses a "winner" from the list

    charges_to_guess_from = [charges[unlucky_number]]
    while len(charges_to_guess_from) != 3:
        ronald = random.randint(0, len(charges)-1)
        if charges[ronald] not in charges_to_guess_from:
            charges_to_guess_from.append(charges[ronald])
    
    return mugshots[unlucky_number], charges[unlucky_number], charges_to_guess_from

if __name__ == '__main__':
    main()