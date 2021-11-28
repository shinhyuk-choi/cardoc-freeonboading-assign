# 원티드x위코드 백엔드 프리온보딩 과제
- 과제 출제 기업 정보
  - 기업명 : 카닥

## Member
| 이름  | github                                   |
|-------|-----------------------------------------|
|최신혁 |[shchoi94](https://github.com/shchoi94)     | 

## 과제 내용
<details>
<summary><b>과제내용 자세히 보기</b></summary>
<div markdown="1">

### **[필수 포함 사항]**
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - **서버 구조 및 디자인 패턴에 대한 개략적인 설명**
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현
  
### 1. 배경 및 공통 요구사항

<aside>
😁 **카닥에서 실제로 사용하는 프레임워크를 토대로 타이어 API를 설계 및 구현합니다.**

</aside>

- 데이터베이스 환경은 별도로 제공하지 않습니다.
 **RDB중 원하는 방식을 선택**하면 되며, sqlite3 같은 별도의 설치없이 이용 가능한 in-memory DB도 좋으며, 가능하다면 Docker로 준비하셔도 됩니다.
- 단, 결과 제출 시 README.md 파일에 실행 방법을 완벽히 서술하여 DB를 포함하여 전체적인 서버를 구동하는데 문제없도록 해야합니다.
- 데이터베이스 관련처리는 raw query가 아닌 **ORM을 이용하여 구현**합니다.
- Response Codes API를 성공적으로 호출할 경우 200번 코드를 반환하고, 그 외의 경우에는 아래의 코드로 반환합니다.

| Response Code  | Description                     |
|-------|------------------------------------------|
|200 OK	|성공
|400 Bad Request	|Parameter가 잘못된 (범위, 값 등)|
|401 Unauthorized	|인증을 위한 Header가 잘못됨|
|500 Internal Server Error	|기타 서버 에러|

---

### 2. 사용자 생성 API

🎁 **요구사항**

- ID/Password로 사용자를 생성하는 API.
- 인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.

```jsx
/* Request Body 예제 */

 { "id": "candycandy", "password": "ASdfdsf3232@" }
```

---

### 3. 사용자가 소유한 타이어 정보를 저장하는 API

🎁 **요구사항**

- 자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.
- 한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다. 즉 사용자 정보와 trimId 5쌍을 요청데이터로 하여금 API를 호출할 수 있다는 의미이다.

```jsx
/* Request Body 예제 */
[
  {
    "id": "candycandy",
    "trimId": 5000
  },
  {
    "id": "mylovewolkswagen",
    "trimId": 9000
  },
  {
    "id": "bmwwow",
    "trimId": 11000
  },
  {
    "id": "dreamcar",
    "trimId": 15000
  }
]
```

🔍 **상세구현 가이드**

- 자동차 정보 조회 API의 사용은 아래와 같이 5000, 9000부분에 trimId를 넘겨서 조회할 수 있다.
 **자동차 정보 조회 API 사용 예제**
  
📄 [https://dev.mycar.cardoc.co.kr/v1/trim/5000](https://dev.mycar.cardoc.co.kr/v1/trim/5000)
  
📄 [https://dev.mycar.cardoc.co.kr/v1/trim/9000](https://dev.mycar.cardoc.co.kr/v1/trim/9000)

📄 [https://dev.mycar.cardoc.co.kr/v1/trim/11000](https://dev.mycar.cardoc.co.kr/v1/trim/11000)

📄 [https://dev.mycar.cardoc.co.kr/v1/trim/15000](https://dev.mycar.cardoc.co.kr/v1/trim/15000)
  
  
- 조회된 정보에서 타이어 정보는 spec → driving → frontTire/rearTire 에서 찾을 수 있다.
- 타이어 정보는 205/75R18의 포맷이 정상이다. 205는 타이어 폭을 의미하고 75R은 편평비, 그리고 마지막 18은 휠사이즈로써 {폭}/{편평비}R{18}과 같은 구조이다.
 위와 같은 형식의 데이터일 경우만 DB에 항목별로 나누어 서로다른 Column에 저장하도록 한다.

  
### 4. 사용자가 소유한 타이어 정보 조회 API

🎁 **요구사항**

- 사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.

</div>
</details>   

## 구현 특이사항
### - 사용자가 소유한 타이어 정보를 저장하는 API   
> - 타이어 정보는 외부 API:https://dev.mycar.cardoc.co.kr/v1/trim/{trimId} 에 의존합니다.   
> 요청 시 마다 각 trimId에 맞게 외부API를 호출하여 타이어 정보를 업데이트하고   
유저가 가진 타이어 관계 정보를 생성합니다.  
현재는 최대 5명 호출이 가능하지만 각기 다른 trimId에 대한 최대 호출개수를 늘리더라도   
외부API I/O로 인한 병목을 최소하하기 위하여   
aiohttp 프레임워크를 사용하여 비동기 방식으로 호출하도록 하였습니다.
### - django 의 view단의 역할을 service, logic 으로 분리   
> - service 역할   
    - 데이터베이스에서 데이터를 얻는다   
    - 도메인 모델을 업데이트 한다   
    - 변경된 내용을 역속화한다.
> - logic 역할   
    - service 의 역할을 제외한 비즈니스 로직
## 사용 기술 및 tools
- Django, DRF, Swagger, sqlite3, aiohttp
## 모델링
![image](./models.png)

## API 문서 (로컬 환경 실행 후)
- http://127.0.0.1:8000/swagger/



## 설치 및 실행 방법
<details>
 <summary><b>설치 및 실행 방법 자세히 보기</b></summary>
<div markdown="1">
  
###  Local 개발 및 테스트용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    $ git clone https://github.com/shchoi94/cardoc-freeonboading-assign.git
    $ cd cadoc-freeonboading-assign
    ```

2. 가상환경 생성 및 프로젝트 실행
    ```bash
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver
    ```


</div>
</details>



# Reference
- 이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 에서 출제한 과제를 기반으로 만들었습니다.
- 본 과제는 저작권의 보호를 받으며, 문제에 대한 정보를 배포하는 등의 행위를 금지 합니다.
