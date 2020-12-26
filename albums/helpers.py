# Function to calculate average rating (out of 5)
def avg_rating(ratings):

    total_ratings = 0

    for i in range(len(ratings)):
        total_ratings += float(ratings[i].rating)
        
    return total_ratings / len(ratings)
