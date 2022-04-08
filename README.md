# RL 그리드 환경
- 그리드 환경의 state, action, reward, transition probability을 제공.
- 주어진 그리드 환경에서 control, prediction 연습용.

<br/>

# 사용 방법
1. class Gridword의 기능
2. 로컬에서 실행하는 방법
3. google colab에서 사용하는 방법

<br/>

## 1. GridWord Methods
> reset()
- 환경의 출력 리셋. 배치된 state는 유지.

<br/>

> get_image() -> numpy.ndarray
- 현재 환경에 대한 이미지를 가져온다.

<br/>

> change_state(pos, state_type)
- pos=(row, col)의 state를 state_type 변경한다.
- state_type은 state의 파생 클래스 type

```python
from state import State
from grid_world import GridWorld

class CustomState(State):
    pass

env = GridWorld((10, 5))
# (3, 3) 위치의 state를 custom으로 변경
env.change((3, 3), CustomState)
```

<br/>

> set_render_value(enable : bool)
- 화면에 각 state에 value(실수값)을 출력 on/off

<br/>

> set_render_policy(enable : bool)
- 화면에 각 state에 policy(실수값)을 출력 on/off

<br/>

> draw_values(state_values : numpy.ndarray)
- 화면에 각 state에 입력을 value값으로 그린다.
- 호출시 자동으로 set_render_value(True)
- state_value의 shape와 env의 (row, col)이 같아야함.

```python
import numpy as np

# 모든 state의 value값이 1인 state-value
values = np.ones(10, 5)

env.draw_values(values)
```


<br/>

> draw_policy(pos, draw_policy : numpy.ndarray)
- 입력 policy로 각 state의 액션확률을 화살표 투명도로 나타낸다.
- 호출시 자동으로 set_render_policy(True)
- assert(draw_policy.shape == (row, col, action_size))
- grid 환경에서는 action size는 4로 고정.

```python
# 각 state의 action 4개의 합이 1인 랜덤확률분포 policy 생성
rands = np.random.random((5, 10, 4))
policy = rands / np.sum(rands,-1, keepdims=True)

env.draw_policy(policy)
```


<br/>


## 2. local graphics
main.py 파일로 main loop 실행
```bash
python -m main
```
- 기본적으로 pygame으로 실시간 랜더링으로 사용.
- main_manager에 put_{key}로 버튼을 매핑해서 사용

<br/>

## 3. google colab
- colab에서 사용시 run, main loop 없이 환경만 생성해서 사용해야함.
- 다음과 같이 환경을 생성해서 상호작용
```python
import grid_world

grid_size = (10, 5)
# colab에서는 반드시 is_render=False
env = GridWorld(grid_size, is_render=False)
```

- GridWorld의 get_image()를 통해 현재 환경이미지를 받아옴.
```python
from state import Goal
from google.colab.patches import cv2_imshow

env.change_state((0, 0), Goal)
screen_image = env.get_image()
cv2_imshow(screen_image)
```

![11](https://user-images.githubusercontent.com/15683086/162460031-0b016b2d-ac34-4040-afc0-914c531aeb11.png)

- state-value 또는 policy를 환경에 그릴 수 있다.

```python
import numpy as np

values = np.zeros(10, 5)
values[4, 1] = -10.1
assert(values.shape == env.state_shape)

env.draw_value(values)
# env.set_render_value(False) 따로 그리지 않을 경우

cv2_imshow(env.get_image())
```

![22](https://user-images.githubusercontent.com/15683086/162486748-5d4ba44c-c994-4f98-9765-bcf7c7b4b3e5.png)

<br/>

- 자세한 구동방법은 RL_grid_world_test.ipynb를 참고

- 이제 자유롭게 환경(state들의 배치)을 구성하고, 구성된 환경에서의 prediction(정해진 policy에 대한 올바른 value 구하기), control(정해진 환경에서의 최적의 policy 구하기)을 구해보자.
