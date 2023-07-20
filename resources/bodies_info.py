celestial_bodies = {
    'Sun': {
        'id': '10',
        'iau_code': '500@0',
        'color': '#FDB813',
        'size': 9
    },
    'Mercury': {
        'id': '199',
        'iau_code': '500@199',
        'color': 'rgb(176, 159, 159)',
        'size': 4
    },
    'Venus': {
        'id': '299',
        'iau_code': '500@299',
        'color': 'rgb(221, 177, 68)',
        'size': 5
    },
    'Earth': {
        'id': '399',
        'iau_code': '500@399',
        'color': 'royalblue',
        'size': 6
    },
    'Mars': {
        'id': '499',
        'iau_code': '500@499',
        'color': 'rgb(220, 85, 82)',
        'size': 5.5
    },
    'Jupiter': {
        'id': '599',
        'iau_code': '500@599',
        'color': 'rgb(129, 77, 77)',
        'size': 7
    },
    'Saturn': {
        'id': '699',
        'iau_code': '500@699',
        'color': 'rgb(155, 113, 46)',
        'size': 6.5
    },
    'Uranus': {
        'id': '799',
        'iau_code': '500@799',
        'color': 'rgb(75, 149, 156)',
        'size': 6.25
    },
    'Neptune': {
        'id': '899',
        'iau_code': '500@899',
        'color': 'rgb(33, 106, 179)',
        'size': 6.3
    },
    'Pluto': {
        'id': '999',
        'iau_code': '500@999',
        'color': 'rgb(161, 71, 71)',
        'size': 3
    },
    'Moon': {
        'id': '301',
        'iau_code': '500@301',
        'color': 'whitesmoke',
        'size': 3.1
    }
}

planets_plot_settings = {
    'terrestrial': {
        'planets': ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars'],
        'axes_range': 2,
        "frame_duration": 50
    },
    'jovian': {
        'planets': ['Sun', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
        'axes_range': 35,
        "frame_duration": 10
    },
    'all': {
        'planets': ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
        'axes_range': 16.25,
        "frame_duration": 20
    }
}
