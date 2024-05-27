from algorithms.colors import COLORS, COLORS_0_4
def get_colors(num=0, opacity = False, nb = None):
    if nb != None :
        if not opacity:
            return COLORS[nb]
        else:
            return COLORS_0_4[nb]
    
    if opacity:
        return COLORS_0_4[:num]
    else :
        return COLORS[:num]


def bar_chart_data(label: list,data_set,subLabel ):
    # plots.bar_chart_data(["first", "second", "third", "fourth"],[[300, 50, 100, 78]],["My First Dataset"])
    # print(data_set)
    return [
        label,
        [
            {
                "label": subLabel[i],
                "data": data,
                "backgroundColor": get_colors(len(label), True),
                "borderColor": get_colors(len(label), False),
                "borderWidth": 1,
            }
            for i, data in enumerate(data_set)
        ],
    ]


def bubble_chart_data( data_set, subLabel=[]):
    if len(subLabel) < len(data_set[0]):
        for i in range(len(subLabel),len(data_set[0])):
            subLabel.append(f'item-{i+1}')
    # data_chart = plots.bubble_chart_data( [[(20, 30, 15), (40, 10, 10)], [(10, 11, 34), (20, 34, 11)]], ["first", "second"])
    return [
        {
            "label": val,
            "data": [{"x": v[0], "y": v[1], "r": v[2]} for v in data_set[i]],
            "backgroundColor": get_colors(nb = i),
        } for i,val in enumerate(subLabel) 
    ]

def doughnut_chart_data():
    pass


def pie_chart_data(label, data, sub_label): 
    # data_chart = plots.pie_chart_data(["label1","label2"],[[21,22]],"sub_label")
    return [
        label,
        [
            {
                "label": sub_label,
                "data": d,
                "backgroundColor": get_colors(len(d)),
                "hoverOffset": 4,
            }
            for d in data
        ]
    ]


def line_chart_data(label: list, data_set, subLabel=[]):
    # line_chart_data = plots.bubble_chart_data( ["first", "second"], [[65, 59, 80, 81, 56, 55, 40],[45, 29, 50, 21, 66, 75, 80]])
    if len(label) < len(data_set[0]):
        for i in range(len(label),len(data_set[0])):
            label.append(f'item-{i+1}')
        
    return [
        label,
        [
            {
                "label": f"label-{i+1}" if len(subLabel) <= i  else subLabel[i],
                "data": data,
                "fill":  "false",
                "borderColor": get_colors(nb=i),
                "tension": 0.1,
            }
            for i, data in enumerate(data_set)
        ],
    ]

def scatter_chart_data(data_set, subLabel=[]):
    if len(subLabel) < len(data_set[0]):
        for i in range(len(subLabel),len(data_set[0])):
            subLabel.append(f'item-{i+1}')
    # data_chart = plots.scatter_chart_data( [[(20, 30), (40, 10)], [(10, 11), (20, 34)]], ["first", "second"])
    return [
        {
            "label": val,
            "data": [{"x": v[0], "y": v[1]} for v in data_set[i]],
            "backgroundColor": get_colors(nb = i),
        } for i,val in enumerate(subLabel) 
    ]


def radar_chart_data(label: list, data_set, subLabel=[]):
    # line_chart_data = plots.radar_chart_data( ["first", "second"], [[65, 59, 80, 81, 56, 55, 40],[45, 29, 50, 21, 66, 75, 80]])
    if len(label) < len(data_set[0]):
        for i in range(len(label), len(data_set[0])):
            label.append(f"item-{i+1}")

    return [
        label,
        [
            {
                "label": f"label-{i+1}" if len(subLabel) <= i else subLabel[i],
                "data": data,
                "fill": 1,
                "backgroundColor": "rgba(186, 170, 227, 0.4)",
                "borderColor": get_colors(nb=i),
                "pointBackgroundColor": get_colors(nb=i),
                "pointBorderColor": "#fff",
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": get_colors(nb=i),
            }
            for i, data in enumerate(data_set)
        ],
    ]


def polar_area_chart_data(label: list, data_set, subLabel):
    # plots.polar_area_chart_data(["first", "second", "third", "fourth"],[[300, 50, 100, 78]],["My First Dataset"])
    if len(label) < len(data_set[0]):
        for i in range(len(label), len(data_set[0])):
            label.append(f"item-{i+1}")
    else:
        label= label[:len(data_set[0])]
    return [
        label,
        [
            {
                "label": subLabel,
                "data": data,
                "backgroundColor": get_colors(len(label)),
            }
            for i, data in enumerate(data_set)
        ],
    ]
