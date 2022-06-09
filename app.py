import PySimpleGUI as sg
import sandpile


# max width and height of grid
WIDTH  = 12
HEIGHT = 9

# default width and height of grid
width = 3
height = 3

# Colors of cells:
# colors = ['black','#4D4D4D','#8CDCDA','#B1D877','#F16A70']
colors = ['#AC92EB','#4FC1E8','#A0D568','#FFCE54','#ED5564']
mode_color = colors[0]

# initialize piles with 0s
piles = [[0 for col in range(width)] for row in range(height)]
memory_piles = [piles]



sg.theme('Black')  

layout_edit = [[sg.Input(
                    0, 
                    key=f'{row},{col}-EDIT-',
                    size=(4,1),
                    justification='center',
                    enable_events=True,
                    visible=True if row < height and col < width else False,
                    background_color=colors[0],
                    text_color='white',
                    font='ariel 40',
                    expand_x = True,
                    expand_y = True) 
                for col in range(WIDTH)] for row in range(HEIGHT)] 

layout_topple = [[sg.Text(
                    0, 
                    key=f'{row},{col}-TOPPLE-',
                    size=(4,1),
                    justification='center',
                    enable_events=True,
                    visible=True if row < height and col < width else False,
                    background_color=colors[0],
                    text_color='white',
                    font='ariel 40') 
                for col in range(WIDTH)] for row in range(HEIGHT)]

layout = [  [
                sg.Text(' width', font='ariel 16'),
                sg.Slider(key='-WIDTH-', 
                          enable_events=True,
                          range=(1,WIDTH), 
                          default_value=3, 
                          orientation='horizontal'),
                sg.Push(),
                sg.Button('topple all', key='-TOPPLE-ALL-')
            ],                
            [
                sg.Text('height', font='ariel 16'),
                sg.Slider(key='-HEIGHT-', 
                          range=(1,HEIGHT), 
                          enable_events=True,
                          default_value=3,
                          orientation='horizontal'),
                sg.Push(),
                sg.Button('add 3 to all', key='-ADD3-')
            ],
            [
                sg.Text('mode:', font='ariel 16'), 
                sg.Button('Edit', key='-EDIT-', disabled_button_color=mode_color), 
                sg.Button('Topple', key='-TOPPLE1x1-', disabled_button_color=mode_color), 
                sg.Push(),
                sg.Button('set all 0', key='-SET0-')
            ],
            [
                sg.Col(layout_edit, key='-EDIT-GRID-'), 
                sg.Col(layout_topple, key='-TOPPLE-GRID-', visible=False)
            ]
          ]

window = sg.Window('Sandpile Toppler', layout, finalize=True)

# initialize mode
mode = '-EDIT-'
window[mode].update(disabled=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # enable previous mode
    window[mode].update(disabled=False)

    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    if event == '-WIDTH-':
        width = int(values['-WIDTH-'])
        # reset piles to 0
        piles = [[0 for col in range(width)] for row in range(height)]
        for row in range(height):
            for col in range(WIDTH):
                if col < width:
                    window[f'{row},{col}-EDIT-'].update(visible=True)
                    window[f'{row},{col}-TOPPLE-'].update(visible=True)
                else:
                    window[f'{row},{col}-EDIT-'].update(visible=False)
                    window[f'{row},{col}-TOPPLE-'].update(visible=False)
    if event == '-HEIGHT-':
        height = int(values['-HEIGHT-'])
        # reset piles to 0
        piles = [[0 for col in range(width)] for row in range(height)]
        for row in range(HEIGHT):
            for col in range(width):
                if row < height:
                    window[f'{row},{col}-EDIT-'].update(visible=True)
                    window[f'{row},{col}-TOPPLE-'].update(visible=True)
                else:
                    window[f'{row},{col}-EDIT-'].update(visible=False)
                    window[f'{row},{col}-TOPPLE-'].update(visible=False)
    if event == '-SET0-':
        piles = [[0 for col in range(width)] for row in range(height)]
    if event == '-ADD3-':
        piles = [[3 + piles[row][col] for col in range(width)] for row in range(height)]
    if event == '-EDIT-':
        mode = '-EDIT-'
        # Show cells for editing and hide cells for toppling
        window['-TOPPLE-GRID-'].update(visible=False)
        window['-EDIT-GRID-'].update(visible=True)
    if event in ('-TOPPLE1x1-', '-TOPPLE-ALL-'):
        mode = '-TOPPLE1x1-'
        # Hide cells for editing and show cells for toppling
        window['-TOPPLE-GRID-'].update(visible=True)
        window['-EDIT-GRID-'].update(visible=False)
    if event == '-TOPPLE-ALL-':
        piles = sandpile.complete_topple(piles)
    for col in range(width):
        for row in range(height):
            # Update piles when editing:
            if event == f'{row},{col}-EDIT-':
                num = values[event]
                if num == '':
                    piles[row][col] = 0
                if num.isnumeric():
                    piles[row][col] = int(num)
            # Topple:
            if event == f'{row},{col}-TOPPLE-':
                piles = sandpile.topple(piles, row, col)
    # update all values in the cells:
    for col in range(width):
        for row in range(height):
            pile = piles[row][col]
            if pile < 4:
                clr = colors[pile]
            else:
                clr =colors[4]
            window[f'{row},{col}-EDIT-'].update(value=pile, background_color=clr)
            window[f'{row},{col}-TOPPLE-'].update(value=pile, background_color=clr)
    # disable the current mode
    window[mode].update(disabled=True)

window.close()
