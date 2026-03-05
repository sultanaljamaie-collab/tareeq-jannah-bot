def get_medal(score):

    if score >= 500:
        return "🏆 عالم كبير"

    if score >= 200:
        return "🥇 عالم"

    if score >= 100:
        return "🥈 طالب علم"

    if score >= 50:
        return "🥉 مبتدئ"

    return "📘 متعلم"
