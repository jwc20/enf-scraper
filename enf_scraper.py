import requests
import csv
from datetime import datetime


def fetch_reviews():
    base_url = (
        "https://api.catchtable.net/api/v3/review/get-review-in-shop?localeCode=en-US"
    )
    page = 1
    all_reviews = []
    while True:
        payload = {
            "page": page,
            "sortingFilter": "B",
            "shopRef": "GH-fb5s4R_O3VqK2Cu8qFw",
            "listSize": 12,
            "isOnlyGlobal": True,
        }
        response = requests.post(base_url, json=payload)
        if response.status_code != 200:
            print(f"Failed to fetch data: HTTP {response.status_code}")
            break

        data = response.json()
        reviews = data.get("data", {}).get("shopReviewList", [])
        if not reviews:
            break  # No more reviews to fetch
        print(reviews)
        all_reviews.extend(reviews)
        page += 1  # Increment page number for next API call

    return all_reviews


def save_to_csv(reviews):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output_{now}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "review_seq",
            "total_score",
            "review_content",
            "reg_date",
            "images",
            "writer_display_name",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for review in reviews:
            images = [img["review_img_url"] for img in review.get("photoList", [])]
            writer.writerow(
                {
                    "review_seq": review.get("review_seq"),
                    "total_score": review.get("total_score"),
                    "review_content": review.get("review_content"),
                    "reg_date": datetime.fromtimestamp(
                        review["reg_date"] / 1000
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    if review.get("reg_date")
                    else "N/A",
                    "images": ", ".join(images),
                    "writer_display_name": review.get("writer_display_name"),
                }
            )
    print(f"Data written to {filename}")


if __name__ == "__main__":
    reviews = fetch_reviews()
    save_to_csv(reviews)
