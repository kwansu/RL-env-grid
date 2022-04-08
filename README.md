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

> draw_values(state_values : numpy.ndarray)
- 화면에 각 state에 입력을 value값으로 그린다.
- state_value의 shape와 env의 (row, col)이 같아야함.

```python
import numpy as np

# 모든 상태가 1인 value를 그린다.
values = np.ones(10, 5)
env.draw_values(values)
```


<br/>

> draw_policy(pos, draw_policy : numpy.ndarray)
- 입력 policy로 각 state의 액션확률을 화살표 투명도로 나타낸다.
- assert(draw_policy.shape == (row, col, action_size))
- grid 환경에서는 action size는 4로 고정.

```python
policy = np.random(10, 5, 4)

env.draw_values(values)
```


<br/>


## 2. local graphics
main.py 파일로 main loop 실행
```bash
python main.py
```
- 기본적으로 pygame으로 실시간 랜더링으로 사용.
- main_manager에 put_{key}로 버튼을 매핑해서 사용

<br/>

## 3. google colab
- colab에서 사용시 run, main loop 없이 환경만 생성해서 사용해야함.
- 다음과 같이 환경을 생성해서 상호작용
```python
import grid_world

grid_size = (5, 6)
# colab에서는 반드시 is_render=False
env = GridWorld(grid_size, is_render=False)
```

- GridWorld의 get_image()를 통해 현재 환경이미지를 받아옴.
```python
from state import Goal
from google.colab.patches import cv2_imshow

env.change_state((0, 0), Goal))
screen_image = env.get_image()
cv2_imshow(screen_image)
```

![11](https://user-images.githubusercontent.com/15683086/162460031-0b016b2d-ac34-4040-afc0-914c531aeb11.png)


