import random
import math
from collections import deque
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = Dash(__name__)

max_len = 50

acc_x = deque(maxlen=max_len)
acc_y = deque(maxlen=max_len)
acc_z = deque(maxlen=max_len)
gyro_x = deque(maxlen=max_len)
gyro_y = deque(maxlen=max_len)
gyro_z = deque(maxlen=max_len)
temp = deque(maxlen=max_len)
prox = deque(maxlen=max_len)
t = deque(maxlen=max_len)

for i in range(max_len):
    acc_x.append(0)
    acc_y.append(0)
    acc_z.append(0)
    gyro_x.append(0)
    gyro_y.append(0)
    gyro_z.append(0)
    temp.append(25)
    prox.append(50)
    t.append(i)

app.layout = html.Div([
    html.H2("Multi-Sensor Dashboard"),
    dcc.Graph(id='imu-graph'),
    dcc.Graph(id='temp-graph'),
    dcc.Graph(id='prox-graph'),
    dcc.Interval(id='interval', interval=500, n_intervals=0)
])

@app.callback(
    [Output('imu-graph', 'figure'),
     Output('temp-graph', 'figure'),
     Output('prox-graph', 'figure')],
    [Input('interval', 'n_intervals')]
)
def update_graph(n):
    time = n

    acc_x.append(math.sin(time/5) + random.uniform(-0.2,0.2))
    acc_y.append(math.cos(time/5) + random.uniform(-0.2,0.2))
    acc_z.append(1 + random.uniform(-0.1,0.1))

    gyro_x.append(random.uniform(-1,1))
    gyro_y.append(random.uniform(-1,1))
    gyro_z.append(random.uniform(-1,1))

    temp.append(25 + math.sin(time/10)*2 + random.uniform(-0.5,0.5))
    prox.append(50 + math.sin(time/3)*20 + random.uniform(-5,5))

    t.append(time)

    imu_fig = go.Figure([
        go.Scatter(x=list(t), y=list(acc_x), mode='lines', name='Acc X'),
        go.Scatter(x=list(t), y=list(acc_y), mode='lines', name='Acc Y'),
        go.Scatter(x=list(t), y=list(acc_z), mode='lines', name='Acc Z'),
        go.Scatter(x=list(t), y=list(gyro_x), mode='lines', name='Gyro X'),
        go.Scatter(x=list(t), y=list(gyro_y), mode='lines', name='Gyro Y'),
        go.Scatter(x=list(t), y=list(gyro_z), mode='lines', name='Gyro Z')
    ])

    temp_fig = go.Figure([
        go.Scatter(x=list(t), y=list(temp), mode='lines', name='Temperature (°C)')
    ])

    prox_fig = go.Figure([
        go.Scatter(x=list(t), y=list(prox), mode='lines', name='Proximity')
    ])

    return imu_fig, temp_fig, prox_fig

if __name__ == '__main__':
    app.run(debug=True)