import datetime, random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 
from django.utils import timezone

from homepage.models import PostTraction
from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from users.models import CustomUser
from user_profile.models import UserProfile

from posts.templates.forms.post_form import NewPostFormLite

def format_number(num=None):
    if num is None:
        num = 55555555

    # If number is less than 1000, return it as it is
    if num < 1000:
        return str(num)
    
    # If number is in thousands (less than a million)
    elif num < 1_000_000:
        # Divide by 1000 and round to one decimal place if necessary
        formatted = round(num / 1000, 1)
        # Return without decimal if it's a whole number
        return f"{int(formatted)}K" if formatted.is_integer() else f"{formatted}K"
    
    # If number is in millions (less than a billion)
    elif num < 1_000_000_000:
        # Divide by 1,000,000 and round to one decimal place if necessary
        formatted = round(num / 1_000_000, 1)
        # Return without decimal if it's a whole number
        return f"{int(formatted)}M" if formatted.is_integer() else f"{formatted}M"
    
    # In case of numbers greater than a billion, you can extend this logic for billions
    else:
        return str(num)

def time_since_post(post):
    now = timezone.now()
    time_diff = now - post.date_posted

    if time_diff < datetime.timedelta(minutes=1):
        # Less than a minute ago
        seconds = int(time_diff.total_seconds())
        return f"{seconds}s"
    
    elif time_diff < datetime.timedelta(hours=1):
        # Less than an hour ago
        minutes = int(time_diff.total_seconds() / 60)
        return f"{minutes}m"
    
    elif time_diff < datetime.timedelta(hours=24):
        # Less than 24 hours ago
        hours = int(time_diff.total_seconds() / 3600)
        return f"{hours}h"
    
    else:
        return None

def create_post_in_post_object(post):
    profile = get_object_or_404(UserProfile, id=post.poster_id)
    account = get_object_or_404(CustomUser, id=profile.user_id)
    
    # Take only the data we need from post object
    post_stripped = {
        "id":post.id,
        "body":post.body,
        "pub_date":post.date_posted,
        "time_since":time_since_post(post)
    }

    # Take only the data we need from user profile object
    profile_stripped = {
        "id":profile.id,
        "display_name":profile.display_name,
        "display_picture":profile.display_picture,
    }

    account_stripped = {
        "username":account.user_name
    }

    combined_post = {
        "post":post_stripped, 
        "poster_profile":profile_stripped, 
        "poster_account":account_stripped,
    }

    return combined_post

def create_quote_post_in_modal_object(post):
    profile = get_object_or_404(UserProfile, id=post.poster_id)
    account = get_object_or_404(CustomUser, id=profile.user_id)
    
    if isinstance(post, Quote):
        post_stripped = {
            "id":post.id,
            "body":post.body,
            "pub_date":post.date_posted,
            "time_since":time_since_post(post),
            "quote_post":create_post_in_post_object(post.quote_post)
        }

    else:
        # Take only the data we need from post object
        post_stripped = {
            "id":post.id,
            "body":post.body,
            "pub_date":post.date_posted,
            "time_since":time_since_post(post)
        }

    # Take only the data we need from user profile object
    profile_stripped = {
        "id":profile.id,
        "display_name":profile.display_name,
        "display_picture":profile.display_picture,
    }

    account_stripped = {
        "username":account.user_name
    }

    combined_post = {
        "post":post_stripped, 
        "poster_profile":profile_stripped, 
        "poster_account":account_stripped,
    }

    return combined_post

def create_combined_profile(request, profile, account, posts_count=None):
    own_account_status = False
    is_following = False
    is_followed = False

    if request.user.get_username() == account.get_username():
        own_account_status = True
    else:
        requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
        requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
        if profile.followers.contains(requester):
            is_following = True
        if profile.following.contains(requester):
            is_followed = True    

    user_profile_stripped = {
        "username": account.user_name,
        "id": profile.id,
        "bio": profile.bio,
        "followers": profile.getFollowers(),
        "following": profile.getFollowing(),
        "location": profile.location,
        "display_picture": profile.display_picture,
        "display_name": profile.display_name,
        "background": profile.background_picture,
        "own_account": own_account_status,
        "is_following": is_following,
        "is_followed": is_followed,
        "dob": account.date_of_birth,
        "doj": account.date_joined,
        "posts_count": format_number(posts_count)
    }

    return user_profile_stripped

def create_combined_profiles(request, profiles):

    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    combined_profiles = []

    for profile in profiles:
        is_following = False
        is_followed = False

        account = get_object_or_404(CustomUser, id=profile.user_id)

        if profile.followers.contains(requester):
            is_following = True
        if profile.following.contains(requester):
            is_followed = True    

        user_profile_stripped = {
            "username": account.user_name,
            "id": profile.id,
            "bio": profile.bio,
            "display_picture": profile.display_picture,
            "display_name": profile.display_name,
            "is_following": is_following,
            "is_followed": is_followed,
        }

        combined_profiles.append(user_profile_stripped)

    return combined_profiles


def create_combined_posts(posts, requester_profile, quote_view=False, quote_view_og_post=None):
    users = [get_object_or_404(UserProfile, id=p.poster_id) for p in posts]
    cusers = [get_object_or_404(CustomUser, id=u.user_id) for u in users]
    comments = [(p.getComments()) for p in posts] 
    reposts = [(p.getReposts() + p.getQuotes()) for p in posts] 
    likes = [(p.getLikes()) for p in posts]
    bookmarks = [(p.getBookmarks()) for p in posts]

    combined_posts = []
    
    for post, profile, account, comments_count, reposts_count, likes_count, bookmarks_count in zip(posts, users, cusers,comments, reposts, likes, bookmarks):
    
        if isinstance(post, Quote):
            post_stripped = {
                "id":post.id,
                "body":post.body,
                "pub_date":post.date_posted,
                "time_since":time_since_post(post),
                "quote_post":create_post_in_post_object(post.quote_post),
                "type": "q"
            }

        elif quote_view:
            post_stripped = {
                "id":post.id,
                "body":post.body,
                "pub_date":post.date_posted,
                "time_since":time_since_post(post),
                "quote_post":create_post_in_post_object(quote_view_og_post),
                "type": "q"
            }

        else:
            # Take only the data we need from post object
            post_stripped = {
                "id":post.id,
                "body":post.body,
                "pub_date":post.date_posted,
                "time_since":time_since_post(post),
                "type": "r"
            }

        if post.poster_id == requester_profile.id:
            post_stripped["own_post"] = "Yes"

        # Take only the data we need from user profile object
        profile_stripped = {
            "id":profile.id,
            "display_name":profile.display_name,
            "display_picture":profile.display_picture,
            "background_picture":profile.background_picture,
        }

        account_stripped = {
            "username":account.user_name
        }

        combined_post = {
            "post":post_stripped, 
            "poster_profile":profile_stripped, 
            "poster_account":account_stripped,
            "comments_count":comments_count,
            "reposts_count":reposts_count,
            "likes_count":likes_count,
            "bookmarks_count":bookmarks_count,
        }
        combined_posts.append(combined_post)

    return combined_posts 

@login_required
def view_posts(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    # popular posts time delta
    pop_post_td = timezone.now() - datetime.timedelta(hours=48)

    # # most popular posts
    # latest_posts_pt = PostTraction.objects.filter(pub_date__gte=pop_post_td).order_by("-score")

    # # most popular friends posts
    # latest_friends_posts = PostTraction.objects.filter()

    # latest_posts = [get_object_or_404(Post, id=pt_post.post_id) for pt_post in latest_posts_pt]

    latest_posts = Post.objects.all().order_by("-date_posted")[:2]
    latest_quotes = Quote.objects.all().order_by("-date_posted")[:20]

    posts = create_combined_posts(latest_posts, requester)
    quotes = create_combined_posts(latest_quotes, requester)
    posts += quotes

    context = {"latest_posts": posts, "new_post_form": NewPostFormLite(), "homepage": True, "profile": create_combined_profile(request, requester, requester_cu), "username": requester_cu.user_name, }
    return render(request, "homepage.html", context)

@login_required
def search(request):
    pass

def view_explore(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    context = {"username": requester_cu.user_name}
    return render(request, "explore.html", context)

@login_required
def populate_site(request):

    posts = [
        'In the heart of the forest, the trees whispered secrets of the ancients.',
        'A cup of coffee in the morning sets the tone for the rest of the day.',
        'The stars above the ocean shimmered like diamonds scattered on velvet.',
        'She danced through the rain as if it were the last day on earth.',
        'Life is a canvas, and you are the artist; paint with bold colors.',
        'The old library was filled with the scent of aged paper and leather-bound books.',
        'He dreamed of far-off places and the adventures they promised.',
        'A gentle breeze carried the scent of wildflowers across the field.',
        'The city skyline glowed with the golden hues of the setting sun.',
        'Every choice leads to a new path; choose wisely, for time never rewinds.',
        'A moment of silence in nature can bring clarity to the noisiest mind.',
        'The cat watched the birds with quiet intensity, its tail flicking rhythmically.',
        'A song can transport you back to a time and place long forgotten.',
        'The mountain peak stood tall and proud, piercing the clouds above.',
        'In the garden, butterflies danced among the blooming roses.',
        'A warm cup of tea is like a hug in a mug, soothing and comforting.',
        'The stars mapped out a story in the night sky, waiting to be told.',
        'In the stillness of dawn, the world feels both new and ancient.',
        'The sound of waves crashing against the shore is the ocean’s heartbeat.',
        'A kind word can change the course of someone’s entire day.',
        'The scent of freshly baked bread filled the kitchen, warm and inviting.',
        'He had a smile that could light up even the darkest corners of the room.',
        'The forest floor was carpeted with moss, soft and cool underfoot.',
        'She stared at the horizon, lost in thoughts that drifted like clouds.',
        'With every step forward, the past seemed to fade just a little more.',
        'The garden was her sanctuary, a place of peace amidst the chaos of life.',
        'Rain tapped gently on the window, a soothing lullaby for the night.',
        'The lighthouse stood resolute against the storm, a beacon of hope.',
        'Books are portals to other worlds, where anything is possible.',
        'A friendship that can weather the storms is a friendship worth keeping.',
        'Sunlight filtered through the leaves, casting a warm glow on the forest path.',
        'The smell of pine needles and earth filled the crisp autumn air.',
        'Each morning is a new beginning, a chance to start fresh.',
        'She collected memories like seashells, each one unique and beautiful.',
        'The road less traveled often leads to the most unexpected destinations.',
        'He found peace in the solitude of the mountains, far from the noise of the city.',
        'Laughter echoed through the room, filling it with warmth and joy.',
        'The river carved its way through the valley, a ribbon of silver in the landscape.',
        'The stars above seemed close enough to touch on that clear, cold night.',
        'Kindness is a language everyone understands, but not everyone speaks.',
        'The fire crackled softly, casting a warm glow in the cozy cabin.',
        'A single act of kindness can ripple out, touching lives in ways unseen.',
        'The meadow was a sea of wildflowers, each bloom a burst of color.',
        'Time spent in nature is never wasted; it replenishes the soul.',
        'The mountain air was crisp and cool, refreshing after the long hike.',
        'Music has a way of expressing what words often cannot.',
        'The full moon lit the path, casting long shadows across the ground.',
        'She wore her heart on her sleeve, open and vulnerable.',
        'The forest hummed with life, each creature playing its part in the symphony of nature.',
        'In a world of noise, silence can be the most powerful sound of all.',
        'The ocean stretched out to the horizon, infinite and untamed.',
        'Each sunset is a reminder that endings can be beautiful too.',
        'The old house creaked with memories of the people who once called it home.',
        'A smile can brighten even the cloudiest of days.',
        'Adventure is out there, waiting for those brave enough to seek it.',
        'The stars were a tapestry of light, woven into the fabric of the night sky.',
        'A garden is a reflection of its gardener, blooming with care and love.',
        'The sound of rain on the roof was a comfort she never grew tired of.',
        'Sometimes, the smallest step in the right direction can be the biggest leap of your life.',
        'A good book is a journey that you can take without ever leaving your chair.',
        'The wind whispered secrets through the trees, carrying stories of old.',
        'Courage is not the absence of fear, but the decision to move forward despite it.',
        'The scent of lavender filled the air, calming and serene.',
        'He carried a pocketful of dreams, each one waiting for its moment.',
        'The mountain trail was steep, but the view from the top was worth every step.',
        'She had a way of seeing the beauty in even the smallest details of life.',
        'The sound of children’s laughter filled the park, carefree and full of joy.',
        'A well-spent day brings peaceful sleep; a life well-lived brings lasting contentment.',
        'The moonlit sea was a mirror, reflecting the stars above.',
        'A true friend is someone who knows the song in your heart and can sing it back to you when you’ve forgotten the words.',
        'The crisp autumn breeze carried the scent of apple orchards and bonfires.',
        'He found joy in the simple things, like the warmth of the sun on his face.',
        'The mountains stood like silent sentinels, watching over the valley below.',
        'In the silence of the early morning, she found clarity and peace.',
        'The river’s song was a lullaby, soothing and constant.',
        'A spark of curiosity can ignite a lifetime of learning.',
        'The old oak tree had stood for centuries, its roots deep and strong.',
        'A handwritten letter is a piece of the past, a tangible connection to someone’s thoughts.',
        'The stars are reminders that even in the darkest night, there is light.',
        'The library was her refuge, a place where she could lose herself in stories and dreams.',
        'A journey of a thousand miles begins with a single step.',
        'The first snow of the season fell softly, blanketing the world in white.',
        'Her laughter was infectious, spreading joy to everyone around her.',
        'In the desert, the silence was vast and overwhelming, yet strangely peaceful.',
        'Every storm runs out of rain, and every challenge has an end.',
        'The city streets buzzed with energy, alive with the sounds of life.',
        'A cup of tea and a good book can make even the stormiest day feel cozy.',
        'She had a quiet strength, like the roots of a tree, grounding her through the storms of life.',
        'The fireflies danced in the warm summer night, tiny beacons of light.',
        'Hope is a whisper in the darkness, reminding you to hold on.',
        'The waves crashed against the rocks with a relentless, rhythmic force.',
        'The smell of fresh pine always reminded him of Christmas mornings.',
        'The desert stretched out before them, vast and endless, under the blazing sun.',
        'A walk through the forest in the fall is a symphony of crunching leaves and bird songs.',
        'The old clock in the corner ticked away the seconds, marking the passage of time.',
        'A cup of hot cocoa was her favorite way to warm up after a cold day.',
        'The horizon was ablaze with the colors of the setting sun, a final farewell to the day.',
        'Her eyes sparkled with mischief, a silent promise of adventure.',
        'The garden was overgrown, wild and free, but beautiful in its chaos.',
        'A life well-lived is one filled with love, laughter, and a little bit of adventure.',
        'The sound of waves lapping against the shore was a lullaby she never tired of.',
        'A single ray of sunlight broke through the clouds, illuminating the path ahead.',
        'The first flowers of spring pushed through the earth, heralding the end of winter.',
        'The road stretched out ahead of them, full of possibilities and unknowns.',
        'A good friend is like a four-leaf clover: hard to find, lucky to have.',
        'The night sky was so clear, they could see the Milky Way stretching out above them.',
        'Her heart raced with excitement as the plane lifted off the ground.',
        'The garden was in full bloom, a riot of color and life.',
        'He stood at the edge of the cliff, staring out at the vast expanse of ocean before him.',
        'The smell of rain on hot pavement always brought back memories of childhood summers.',
        'The city was alive with lights and sounds, a cacophony of life and energy.',
        'A cup of hot coffee on a cold morning is one of life’s simplest pleasures.',
        'The forest was quiet, except for the soft rustling of leaves in the breeze.',
        'A smile is the universal language of kindness.',
        'The sunset painted the sky in shades of pink, orange, and purple.',
        'Her laughter filled the room, bright and full of joy.',
        'The old barn creaked in the wind, its weathered wood telling stories of years'
        'In the quiet of the early morning, the world feels like it’s holding its breath.',
        'The fire crackled in the hearth, casting a warm glow on the room.',
        'A moment of peace in nature can heal the soul in ways words never could.',
        'The sound of a crackling fire and the smell of wood smoke filled the air.',
        'She stood at the water’s edge, letting the waves lap at her feet.',
        'The mountain loomed in the distance, its peak shrouded in mist.',
        'A book is a dream that you hold in your hands.',
        'The forest was a cathedral of green, the trees reaching towards the sky.',
        'A gentle rain began to fall, its soft patter a soothing melody.',
        'The moon hung low in the sky, casting a silver glow over the landscape.',
        'A smile from a stranger can brighten even the darkest of days.',
        'The stars flickered in the night sky like tiny beacons of hope.',
        'A true friend is someone who sees the pain in your eyes while everyone else believes the smile on your face.',
        'The forest was alive with the sounds of nature, a symphony of birdsong and rustling leaves.',
        'The mountains stood tall and proud, their peaks reaching towards the heavens.',
        'A cup of tea and a cozy blanket make for a perfect rainy day combination.',
        'The old house was filled with memories, the walls whispering stories of the past.',
        'In the stillness of the night, the world seemed at peace, if only for a moment.',
        'The river wound its way through the valley, a ribbon of silver in the twilight.',
        'A good laugh is sunshine in the house.',
        'The clouds parted, and a single ray of sunlight pierced the darkness.',
        'A journey through the forest reveals secrets only nature can tell.',
        'The sound of the ocean was a constant, soothing presence.',
        'The air was filled with the scent of blooming jasmine, sweet and intoxicating.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse a ligula leo. Donec molestie nisl ac dolor ultricies ultrices. Aliquam iaculis, nibh sed tincidunt tempor, erat nibh sollicitudin enim, non tincidunt leo enim sit amet et.'
    ]


    unique_usernames = [
        'StarBlaze5', 'BrightMoon', 'Galacticine8', 'CrimsonSky', 'FrozenMist', 'StarEcho7', 'CelestialPe9', 'NebulaBlaze6', 'StarShine7', 'GalacticStor', 'NebulaBlaze8', 'VortexSpin', 'StarrySky5', 'GalicBlaze', 'IceDragon5', 'StarStorm6', 'ShadowBlaze', 'StarBlaze9', 'GalacticRay', 'ShiningSky', 'LunarPulse5', 'EclipseStom7', 'StarShine8', 'SolarGlow9', 'ShadowStorm', 'BoldTiger9', 'MeteorRay5', 'MeteorNova8', 'FrostyRay9', 'FrostBlaze6', 'IceQueen23', 'GacticBlaze5', 'NovaRay', 'ShadowPulse', 'ShadowGlow7', 'SolarBlaze5', 'StarFire7', 'MeteorShine6', 'EclipseGlow8', 'LunarFire', 'LunarPulse', 'EclipseSun', 'Celestiaine9', 'StarNova', 'alacticWave8', 'GoldenAura', 'MeteorRay9', 'ShadowStorm9', 'LunarNova', 'DarkKnight7', 'Celestihine5', 'WildFlame9', 'BoldHero9', 'GaacticNova6', 'SolarGlow', 'GlowingSky', 'UrbanChic5', 'Starlight7', 'GoldenSun', 'CelestiaNova', 'NebulaFire8', 'Electric7', 'JollyRanchr', 'MeteorGlow8', 'StarFire8', 'ThunderBolt', 'NebulaShin5', 'LunarRay6', 'MeteorPulse6', 'FrostPulse7', 'CeletialFire', 'NebulaShine9', 'NebulaGlow', 'CeleslStorm5', 'EagleHunter', 'EclipseFire9', 'NinjaTurtle', 'LunarShine6', 'NebulaRay9', 'SunnySky12', 'GcticGlow9', 'EclipseFire7', 'GacticShine5', 'RockStar44', 'NebulaFire5', 'ShadowPulse6', 'EclipseGlow6', 'MeteorShine5', 'MeteorShine', 'Wanderlust', 'NovaGlow5', 'Firefly55', 'CelestialGw6', 'ThunderBird', 'GacticStorm8', 'ShadowGlow9', 'EclpsePulse6', 'FrostBlaze9', 'MysticWave', 'MysticFrost', 'EchoWave19', 'MeteorGlow6', 'GalacticRay9', 'CoolBreeze8', 'FrostyWind', 'LunarStorm6', 'SunnyDay34', 'GlacticGlow8', 'WildHunter', 'MeteorPulse8', 'RapidTiger', 'CelesalEcho7', 'MeteorFire5', 'GaacticFire9', 'CelestialRa5', 'NebulaRay', 'CrazyFox32', 'GalaticNova8', 'NebulaBlze5', 'EclipseRay8', 'StarPulse5', 'CelestialWe7', 'DreamWeaver', 'LunarGlow5', 'FrostPulse', 'CetialBlaze8', 'SkyWalker27', 'SolarStorm5', 'FrostyPaws', 'Galacticire7', 'NebulaRay5', 'EcliseFire6', 'LunarShine8', 'StarFire5', 'GamerGirl7', 'MightyLion', 'SolarRay6', 'GalactiNova9', 'GalacticRay7', 'CeleialNova6', 'LunarPulse8', 'StarGlow5', 'SolarPulse7', 'SolarRay8', 'SeaBreeze9', 'GalacticSto5', 'BrightStar', 'ElipsePulse5', 'EclipePule9', 'StarNova9', 'LunarEcho', 'NebulaRay8', 'GalaccPulse7', 'OceanWhale', 'LunarBlaze', 'EclipseRay9', 'CeleialNova9', 'LunarShine5', 'EclipseStrm5', 'StarGlow8', 'CloudWalker', 'EclpsePulse7', 'EclipseNova', 'GalcticNova5', 'MightyMouse', 'CeleslBlaze7', 'EclipeBlaze9', 'LunarGlow8', 'SunnyMeadow', 'FrostFlare', 'alacticGlow5', 'StarFire6', 'NebulaPulse7', 'NebulaFire7', 'EclipseNova5', 'CeleialWave5', 'DaringDuke', 'SolarRay9', 'GalacticPse5', 'StarBlaze', 'NebulaGlow7', 'CelestialX', 'SilentWolf', 'EclipseNova7', 'LunarShine9', 'SolarRay5', 'NebulaFire9', 'OceanVista', 'EclipseNova8', 'GalaccBlaze7', 'MagicWand2', 'CelestialGl8', 'StarFire9', 'SolarStorm8', 'StarBurst1', 'CstialPulse5', 'GalaicPulse8', 'LunarRay', 'SolarStorm', 'StarEcho5', 'FalconEye4', 'SwiftRiver', 'FireWaves', 'SolarEcho', 'StarGazer6', 'EclipeStorm8', 'SolarShine', 'LunarStorm8', 'LunarPulse6', 'LunarNova5', 'MeteorStorm7', 'MeteorStorm6', 'StarNova8', 'MeteorNova7', 'GalcticWave7', 'Galactiulse6', 'NovaWave7', 'GoldenEye8', 'DreamRay5', 'LunarRay5', 'EclipseBlae8', 'FireStar7', 'Eclipseulse8', 'StarStorm7', 'ShadowGlow', 'CosmicHawk', 'CestialNova5', 'NebulaFire6', 'BrightEyes', 'FrostRay', 'NebulaShine7', 'MightyEagle', 'CelestBlaze9', 'NebulaNova5', 'GalactiRay5', 'GalacticRay6', 'MeteorEcho', 'LunarWave9', 'NebulaWave', 'MeteorGlow5', 'StarShine9', 'EagleEye12', 'LunarRay7', 'CelestiWave9', 'FrostGlow6', 'ZenithStar', 'FrostBlaze8', 'StarPulse9', 'FrostRay5', 'WickedStorm', 'StarStorm8', 'Celestiulse8', 'MeteorFire7', 'CeleialEcho6', 'DreamStorm', 'LunarStorm5', 'SolarBlaze7', 'CetialStorm9', 'NebulaPulse8', 'NebulaGlow6', 'CelestialWe8', 'EclipseGlow5', 'GalacticPse', 'CstialPulse7', 'SolarPulse6', 'FrostRay7', 'NobleQuest', 'MeteorNova', 'MysticFlame', 'FrozenSun', 'FireWave5', 'ShadowRay5', 'MysticKnight', 'MeteorNova5', 'CestialWave6', 'CosmicEcho', 'NebulaGlow5', 'StarBlaze8', 'MeteorEcho5', 'CelestialGl7', 'NightOwl6', 'QuickFox88', 'Celestial2', 'LunarEclipse', 'NebulaStorm5', 'ShadowFire9', 'GalacticX', 'LunarSh', 'SpaceHero6', 'LunarPulse7', 'GalacticShin', 'StarNova6', 'LunarStorm7', 'Thunder01', 'MeteorRay7', 'StormChaser', 'LunarBlaze6', 'LunarNova9', 'QuantumLeap', 'CloudDream', 'MeteorGlow7', 'SolarPulse8', 'CelestiaRay9', 'ZenMaster4', 'SolarBlaze6', 'IceFire3', 'Glimmer9', 'Jetstream2', 'GalacticStm7', 'WindWalker', 'WildLynx8', 'LunarGlow6', 'NebulaBlaze', 'GalactcGlow', 'FrostFire5', 'IceStorm8', 'LunarRay8', 'CosmicShine', 'Celestialay6', 'EclipseGlow7', 'LoneWolf56', 'NebulaPulse9', 'MeteorStorm', 'NebulaShine8', 'StellarRay', 'EclipseWave', 'HappyPanda', 'LunarNova7', 'StarNova5', 'UrbanNinja', 'BlueOcean7', 'NebulaRay6', 'FireStorm3', 'NovaLight', 'NebulaBlaze9', 'LunarStorm', 'SolarStorm7', 'MeteorRay6', 'EclipseNova9', 'EclipsShine5', 'LunarGlow7', 'GalacticWave', 'FrostShine7', 'GalacticFir5', 'GalaxyRider', 'EclipseRay', 'BrightRay', 'CelestialEc5', 'StarGlow9', 'GalaicBlaze', 'StormRider', 'SwiftHawk2', 'ShiningMoon', 'NebulaPulse6', 'CstialBlaze5', 'CelialStorm7', 'MeteorStorm5', 'TurboJet5', 'Eclipsetorm6', 'StarPulse8', 'CeltialEcho9', 'MeteorPulse5', 'LunarBlaze7', 'MeteorShine9', 'ShiningStar', 'CestialNova7', 'EclipseRay6', 'NebulaNinja', 'Celestialhin', 'GalacicNova7', 'Celestial3', 'EclipseBlze7', 'CosmicFire', 'SolarStorm9', 'NebulaRay7', 'MeteorGlow9', 'NebulaStorm', 'GlacticBlaze', 'StarStorm9', 'MeteorFlare', 'SolarRay7', 'Celestialave', 'NebulaSky5', 'MeteorStorm8', 'MeteorShine7', 'MeteorRay8', 'ShadowKnight', 'TechGuru12', 'EclipseBlaze', 'StarNova7', 'NebulaBlaze7', 'SolarBlaze9', 'NebulaNova7', 'NebulaStorm8', 'EclipseRay5', 'JaneDoe22', 'FrostNova', 'CosmicPulse', 'CestialGlow9', 'StarBlaze7', 'SolarStorm6', 'LunarNova8', 'MagicMan9', 'Celestial1', 'ShadowDance', 'Sunrise12', 'NebulaGlow9', 'ElectricBlue', 'CelestlFire5', 'GacticShine9', 'NebulaPulse5', 'FrostyGlow8', 'SolarGlow7', 'CelestlBlaze', 'SolarPulse', 'CelestialFir', 'CelealBlaze6', 'GacticBlaze8', 'CeletialGlow', 'FrostStorm5', 'ClestialRay8', 'NebulaShine', 'StormFlare', 'StarPulse6', 'GalaxyGlow', 'EclipsePulse', 'CoolCat13', 'MysticMoon', 'VortexStorm', 'CelestialSt6', 'AlphaWolf2', 'NebulaStorm6', 'LunarShine7', 'lestialNova8', 'LunarGlow9', 'FrostWave', 'NebulaGlow8', 'MeteorPulse9', 'MeteorStorm9', 'CstialShine7', 'Jester123', 'Electric3', 'StarBlaze6', 'FireBird2', 'EclipseGlow9', 'FrostGlow5', 'FrostShine5', 'LunarNova6', 'GalacticSto6', 'GalactiGlow6', 'GacticStorm9', 'SolarFlare', 'MeteorPulse7', 'SolarPulse9', 'StarPulse7', 'ThunderRay', 'DreamCatcher', 'MeteorShine8', 'MeteorNova6', 'MeteorFire9', 'StarShine5', 'StarGlow6', 'LunarRay9', 'SolarGlow8', 'ShadowGlow5', 'MeteorFire8', 'RedDragon7', 'StarShine6', 'CelestilStor', 'NebulaNova6', 'CelestPulse6', 'NebulaShine6', 'SolarGlow6', 'StarGazer1', 'SolarGlow5', 'StarGlow7', 'LunarStorm9', 'GalaticRay8', 'alacticPulse'
    ]

    emails = []

    display_pictures = ['user1.jpg','user2.jpg','user3.jpg','user4.jpg','user5.jpg','user6.jpg','user7.jpg','user8.jpg','user9.jpg','user1.avif']

    background_pictures = ['bg_1.jpg','bg_2.jpg','bg_3.jpg','bg_4.jpg','bg_5.jpg','bg_6.jpg','bg_7.jpg','bg_8.jpg','bg_9.jpg','bg_10.jpg']

    i = 0
    if CustomUser.objects.filter(user_name=unique_usernames[0]).count() == 0:
        # create the dummy account
        for username in unique_usernames:
            email = username + '@tweetstaff.com'
            emails.append(email)
            dum_user = CustomUser.objects.create_user(
                email=email,
                user_name=username,
                date_of_birth=datetime.datetime(1999, 5, 26, 21, 12, 33, 675765, tzinfo=None),
                password='foo'
            )

            dum_profile = get_object_or_404(UserProfile, user_id=dum_user.id)
            dum_profile.display_name = username
            dum_profile.display_picture = display_pictures[i % len(display_pictures)]
            dum_profile.background_picture = background_pictures[i % len(background_pictures)]

            dum_profile.save()

            # Posts 1-5
            num_posts = random.randrange(1, 5)
            user_posts_index = [random.randrange(0,140) for i in range(num_posts)]
            for index in user_posts_index:

                post = Post(
                    poster = dum_profile,
                    body=posts[index]
                )

                post.save()

            i+=1
        

    for emailA in emails[:10]:
        user_cu = get_object_or_404(CustomUser, email=emailA)
        profile = get_object_or_404(UserProfile, user_id=user_cu.id)

        print("", profile.display_name, profile.display_picture, profile.background_picture)


    print("count: ", len(posts), len(unique_usernames))
    return redirect(reverse('homepage:home'))

