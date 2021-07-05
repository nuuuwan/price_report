"""Tweet."""


from utils import twitter, timex

from price_report import bpi


def _tweet():
    date_id = timex.get_date_id()
    bpi_info = bpi._compute_index(date_id)
    date = bpi_info['rice']['date']

    price_mackerel = bpi_info['mackerel']['price_per_si_unit']
    price_mackerel_tin = (float)(price_mackerel) * 0.425

    tweet_text = '''Basic බත් Index (β) ({date})

🍚 Samba Rice: {price_rice:.0f} LKR/kg
🍲 Dhal: {price_dhal:.0f} LKR/kg
🐟 Mackerel: {price_mackerel:.0f} LKR/Tin (425g)

🍛 Basic බත්: {price_bpi:.0f} LKR*

* Retail Price of 1 cup (200g) Rice, 50g Dhal, ⅕ Tin (85g) Mackerel

Price Source: Supermarkets in #Colombo

#lka #SriLanka'''.format(
        date=date,
        price_rice=(float)(bpi_info['rice']['price_per_si_unit']),
        price_dhal=(float)(bpi_info['dhal']['price_per_si_unit']),
        price_mackerel=price_mackerel_tin,
        price_bpi=bpi_info['bpi_price'],
    )
    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        update_user_profile=True,
    )


if __name__ == '__main__':
    _tweet()
