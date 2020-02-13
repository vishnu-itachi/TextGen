from django.http import HttpResponse
from django.template import loader
import time
from threading import Thread


def genfun(place, testlen, percentage, aspect_list):
    s = "The place is " + place + ". " + "The textlength is : " + testlen + \
        ". " + "Percentage of male comments is : " + percentage + "%. "
    s += "The aspects are : "
    for aspect in aspect_list:
        s += aspect + ", "
    s = s[:-2]
    s += "."
    return s


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


def sample():
    sentences = [
        ['220122028_12', "Taxi's are also allowed to stop during the day and the dodgy bus station is nowhere near as bad in daylight !",
         21, 0.4426337403068801, 'female', 'Europe', 'neg', 'amenities', 'taxis'],
        ['657080342_13', 'There is a cafe selling drinks , meals and snacks a few steps below the top level , which was handy as we were at the summit around lunchtime .',
         29, 0.5803618297310675, 'male', 'Europe', 'neg', 'amenities', 'cafe'],
        ['542913782_3', 'Walking the steps brings you great photo ops , touristy shops and several cafes .',
         14, 0.23947007919485233, 'male', 'UNK', 'pos', 'amenities', 'cafes'],
        ['444925733_2', 'We were surprised by the number of well-priced modern bars and the nice gift shops that deserve approval .',
         18, 0.35070206814057087, 'female', 'Europe', 'neg', 'amenities', 'shops'],
        ['410291223_5', 'Vans go to and from other locations but the square is pretty with two flower kiosks and is very beautiful and safe .',
         22, 0.4565490414123081, 'male', 'UNK', 'pos', 'amenities', 'kiosks'],
        ['387174692_4', 'A few souvenir shops at the top as well as a cafe which has great fresh juices such as mango juice and acai .',
         23, 0.39533471539349946, 'male', 'North America', 'pos', 'amenities', 'shops'],
        ['295894030_2', 'Many lookout spots , a few cafes for snacks& drinks , souvenir shops and a small holly room for prayer .',
         20, 0.443875956937799, 'male', 'North America', 'neg', 'amenities', 'cafes'],
        ['165133350_5', 'Tambin hay una casa de souvenirs y algunos lugares para tomar algo .',
         12, 0.19676784029038114, 'male', 'South America', 'neg', 'amenities', 'souvenirs'],
        ['163260972_3', 'I chose to take the 120 + steps , which offered rest stops with great views along the way .',
         19, 0.38619416927899686, 'male', 'UNK', 'pos', 'amenities', 'stops'],
        ['157466183_4', 'The souvenirs store is expensive , you can find a lower price near the beach and in local stores around the city .',
         22, 0.6066132453390529, 'female', 'North America', 'neg', 'amenities', 'stores']
    ]

    para = []
    for l in sentences:
        temp = l[1].replace(l[-1], '<b>'+l[-1]+'</b>')
        if(l[-5] == 'male'):
            temp = "<span class = 'male'>" + temp + "</span>"
        else:
            temp = "<span class = 'female'>" + temp + "</span>"
        para.append(temp)

        paragraph = ''.join(para)
    time.sleep(2)
    return paragraph


# @start_new_thread
def index(request):
    context = {}
    place = ''
    Text_len = 200
    percentage = 50
    aspect_list = []
    context = {
        'Text_len': Text_len,
        'percentage': percentage,
        'aspect_list': aspect_list,
        'paragraph': ''
    }

    if(request.GET):
        print(request.GET)
        # place = request.GET['wonder'],
        place = request.GET.get('wonder', False),
        # Text_len = request.GET['len'],
        Text_len = request.GET.get('len', False),
        percentage = request.GET.get('perlen', False),
        aspect_list = request.GET.getlist('aspect')
        if(len(aspect_list) == 0):
            # print("empty list")
            aspect_list = ['attractions', 'access', 'activities',
                           'amenities', 'culture', 'cost', 'problem']
        context = {
            'Text_len': Text_len[0],
            'percentage': percentage[0],
            'aspect_list': aspect_list,
            'paragraph': sample()
        }
    template = loader.get_template('gen/index.html')
    return HttpResponse(template.render(context, request))
