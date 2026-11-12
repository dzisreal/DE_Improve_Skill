# Tuần 1 — Grain, thời gian, Python và retry

Tuần 1 của [lộ trình VinFast](vinfast-8-week-plan.md): **7 buổi × 120 phút**.
Đầu ra là bài SQL/Python có thể chạy, tests và lời giải thích của người học.
Chưa cần Docker, ClickHouse, tài khoản cloud hoặc cài thêm skill.

## Cách học cùng Codex

Mỗi ngày 1–6: 20 phút đọc/ôn, 70 phút tự làm, 20 phút test/giải thích, 10 phút
learning log tiếng Anh. Ngày 1 dành 10 phút trong phần tự làm để kiểm tra môi
trường. Khi bế tắc, gửi code đang có, expected/actual output và giả định; xin
một gợi ý rồi thử tiếp. Không yêu cầu AI viết hoàn chỉnh trước khi tự làm.

Prompt mở buổi: “Dùng $socratic-tutor hướng dẫn ngày N trong
docs/learning/week-01-foundations.md. Hỏi một câu kiểm tra hiểu biết trước,
cho tôi tự làm rồi mới gợi ý. Chưa đưa lời giải đầy đủ. Cuối buổi yêu cầu tôi
giải thích một counterexample và tự sửa code.”

Prompt review: “Dùng $data-review review SQL của tôi theo grain, version và
thời gian. Đưa fixture chứng minh lỗi. Phân biệt điều đã chạy với suy luận.”
Skills là tùy chọn; bài tập vẫn làm được bằng editor và Python.

## Chuẩn bị trên Linux và macOS

Dùng Git và Python 3.9+ có module `sqlite3`, SQLite 3.25+ để hỗ trợ window
functions. Dùng interpreter hiện có nếu đạt; không thay Python hệ thống. Nếu
thiếu Python, Linux dùng package manager của distro, macOS dùng bản cài từ
[python.org](https://www.python.org/downloads/macos/) hoặc Homebrew đã có sẵn.
Không cần pip package hay virtualenv cho fixture này. Lệnh chung trong Terminal:

```sh
git clone https://github.com/dzisreal/DE_Improve_Skill.git
cd DE_Improve_Skill
git switch docs/vinfast-8-week-plan
python3 -c "import sqlite3, sys; print(sys.version); print(sqlite3.sqlite_version); assert sys.version_info >= (3, 9); assert sqlite3.sqlite_version_info >= (3, 25)"
```

Nếu đã clone, dùng checkout đó; với working tree sạch chạy `git fetch origin`
rồi `git switch docs/vinfast-8-week-plan` và `git pull --ff-only`. Không reset
bài làm chưa commit. Khi bắt đầu bài tập, tạo nhánh riêng:

```sh
git switch -c learn/week01-foundations
mkdir -p exercises/week01 docs/learning/evidence
```

Tên nhánh/path là quy ước cho bài làm sẽ tạo, chưa phải code đã triển khai sẵn.
Nếu nhánh đã tồn tại, switch về nhánh đó thay vì tạo lại. Sau khi PR kế hoạch
được merge, có thể bắt đầu nhánh học từ `main` đã cập nhật.

Sao chép block sau vào `exercises/week01/day01.py`, rồi chạy
`python3 exercises/week01/day01.py`. Đây chỉ là fixture và truy vấn kiểm tra
load; người học sẽ thay `query` bằng lời giải. Database ở RAM, chạy lại tạo
một database mới; lưu code và output cần review, không cần lưu file database.

```python
import sqlite3

connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE telemetry (
    event_id TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    event_time TEXT NOT NULL,
    ingested_at TEXT NOT NULL,
    version INTEGER NOT NULL,
    distance_delta_km REAL NOT NULL
);
CREATE TABLE vehicle_dealer_history (
    vehicle_id TEXT NOT NULL,
    dealer_id TEXT NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT NOT NULL
);
""")
rows = [
    ("e10", "car1", "2026-11-01T10:00:00Z", "2026-11-01T10:01:00Z", 1, 7.0),
    ("e10", "car1", "2026-11-01T10:00:00Z", "2026-11-01T10:01:00Z", 1, 7.0),
    ("e10", "car1", "2026-11-01T10:00:00Z", "2026-11-01T10:07:00Z", 2, 9.0),
    ("e11", "car1", "2026-11-01T09:55:00Z", "2026-11-01T10:08:00Z", 1, 2.0),
    ("e12", "car2", "2026-11-01T10:00:00Z", "2026-11-01T10:02:00Z", 1, 4.0),
]
connection.executemany("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", rows)
connection.executemany(
    "INSERT INTO vehicle_dealer_history VALUES (?, ?, ?, ?)",
    [
        ("car1", "A", "2026-01-01T00:00:00Z", "2026-11-01T10:00:00Z"),
        ("car1", "B", "2026-11-01T10:00:00Z", "9999-12-31T00:00:00Z"),
        ("car2", "C", "2026-01-01T00:00:00Z", "9999-12-31T00:00:00Z"),
    ],
)
connection.commit()
query = "SELECT COUNT(*) AS raw_rows FROM telemetry"
print(connection.execute(query).fetchall())  # Fixture load must print [(5,)].
connection.close()
```

Timestamp của fixture cố định format UTC `Z` nên phép so sánh chuỗi giữ đúng
thứ tự thời gian. Khi nhận input nhiều timezone/format, phải parse và chuẩn hóa;
không áp dụng giả định này cho mọi chuỗi timestamp. SQLite dùng để luyện logic,
không chứng minh ClickHouse storage semantics hoặc hành vi Spark connector.

## Ngày 1 — Grain và lựa chọn version

**Học:** grain của raw record, logical event và aggregate; event time vs ingestion
time vs version; `ROW_NUMBER`, grouping và ties.

**Làm:** từ fixture, tự tính kết quả trên giấy trước. Viết query lấy trạng thái
mới nhất của mỗi event, rồi tổng distance theo vehicle/ngày UTC. Viết query sai
dùng `MAX(event_time)` và chỉ ra các dòng bị giữ thừa. Không sửa bằng `DISTINCT`
ở cuối mà chưa giải thích duplicate xuất hiện từ đâu.

**Tự kiểm:** raw có 5 dòng, canonical có 3 logical events. Chèn thêm một bản
duplicate giống hệt thì tổng không đổi. Nếu cùng event/version nhưng payload
khác, nêu quy tắc conflict thay vì chọn một dòng tùy ý. Với bài cơ bản,
`event_id` là global logical key, vehicle/event_time không đổi giữa các version.

**Nộp:** `day01.py` hoặc SQL kèm harness, expected/actual output, ba câu mô tả
grain ở từng bước. Kết thúc tự giải thích vì sao version mới không cần event
time mới.

## Ngày 2 — Incremental và late data

**Học:** watermark dùng để tìm input khác với version dùng để resolve state;
event-day bị ảnh hưởng có thể nằm trong quá khứ. Trong bài này `ingested_at`
được gán tại hệ thống nhận, cố định, và toàn bộ fixture có sẵn.

**Làm:** chia batch A gồm dòng có ingestion time đến 10:02; batch B gồm phần
còn lại đến 10:08. Xây current-event state và mart, chạy A → B → B. So sánh với
full rebuild A+B. Viết test cho late e11 và correction e10; thử cách sai chỉ
đọc `event_time > 10:00` để thấy mất dữ liệu.

**Tự kiểm:** kết quả cuối hai cách phải giống nhau; replay B không tăng metric.
Không cộng toàn bộ version mới vào tổng cũ mà quên trừ/replace trạng thái trước.
Giải thích checkpoint cập nhật khi nào và làm gì nếu hai record có cùng
ingestion timestamp. Lab có thể replay overlap rồi dedup; production cần
contract nguồn/manifest/offset rõ ràng, không coi timestamp đơn lẻ là đủ.

**Nộp:** `day02.py`, assertions full vs incremental/replay và sơ đồ state trước/
sau từng batch. Ngày này chưa yêu cầu cài Airflow.

## Ngày 3 — SCD2 và biên thời gian

**Học:** khoảng `[valid_from, valid_to)`, point-in-time join, current flag,
non-overlap, late dimension changes.

**Làm:** join canonical events với `vehicle_dealer_history` theo event time.
Kiểm tra event tại 09:59:59, 10:00:00 và 10:00:01. Sau đó cố tình thêm một
khoảng chồng nhau và viết kiểm tra phát hiện; không âm thầm chọn bản start nhỏ
hơn. Thêm trường hợp gap để phân biệt không tìm thấy dimension với nhân đôi fact.

**Tự kiểm:** mỗi fact khớp đúng một dimension khi history hợp lệ; tổng distance
trước/sau join không bị nhân lên. Test overlap fail khi có lỗi, pass sau khi
sửa fixture. `is_current` chỉ cho hiện trạng, không thay điều kiện join lịch sử.

**Nộp:** `day03.py`, boundary/overlap/gap tests và ADR ngắn giải thích half-open
interval thay vì kết thúc một phút trước bản kế tiếp.

## Ngày 4 — Python validation và quarantine

**Học:** type hints, exceptions có chủ đích, lỗi cú pháp JSON khác lỗi contract,
pure transform và error record có thể truy vết.

**Làm:** viết `normalize_line(line, line_number)` với interface tự chọn, trả
record hợp lệ hoặc lỗi có `line_number`/`error_code`. Yêu cầu ID không rỗng,
version integer dương (không nhận boolean), distance hữu hạn không âm,
timestamp có timezone và được chuẩn hóa UTC. Parse JSON thành công chưa đủ.
Không log nguyên payload khi có dữ liệu cá nhân; fixture chỉ dùng dữ liệu giả.

**Tự kiểm:** ít nhất 6 cases: valid, JSON hỏng, thiếu ID, version không hợp lệ,
timestamp thiếu timezone, distance âm/không hữu hạn. Bản hỏng không làm mất các
bản tốt còn lại; lỗi I/O không bị nuốt như thể tất cả dữ liệu đã xử lý xong.

**Nộp:** `normalize.py`, `test_normalize.py` dùng `unittest` và lệnh chạy:
`python3 -m unittest discover -s exercises/week01 -p 'test_*.py' -v`.
Có thể gom thêm edge cases bằng subtests, không cần framework mới.

## Ngày 5 — Streaming và tách I/O

**Học:** iterator/generator, đọc theo dòng, bounded batch và nơi dữ liệu có thể
vẫn tích tụ dù đầu vào là generator.

**Làm:** tách ba phần: đọc lines, normalize, ghi valid/quarantine. Transform
nhận iterable để test bằng generator trong RAM, không phụ thuộc đường dẫn file
hoặc S3. Tránh `read()`/`readlines()` toàn file và tránh append toàn output vào
list; chọn batch size có giới hạn nếu sink cần ghi batch.

**Tự kiểm:** dùng iterator đếm số lần đọc để chứng minh lấy kết quả đầu không
tiêu thụ hết input. Chạy 1 nghìn rồi 100 nghìn record sinh tuần tự; ghi peak
Python allocation bằng `tracemalloc` và tổng valid/error counts. Đây không phải
RSS toàn process; không dùng nó để kết luận bộ nhớ Spark hoặc native libraries.

**Nộp:** streaming pipeline, test laziness/counts và số đo; giải thích nơi nào
không được giữ unbounded state. Packaging đầy đủ chuyển sang tuần 2.

## Ngày 6 — Thất bại, commit và replay

**Học:** transaction boundary, external side effects, task status, idempotency
và checkpoint. Simulation này minh họa cơ chế, chưa phải kiểm chứng Spark.

**Làm:** với SQLite và một target table không unique constraint, thử hai cách
ghi 3 records: (A) một transaction, commit cuối, rollback rõ ràng khi lỗi;
(B) commit từng record. Cố tình raise sau record thứ hai, trước record thứ ba.
Quan sát target trong cùng connection trước khi close; ghi row counts sau xử lý
exception, trước replay. Sau đó replay toàn bộ batch và xem cách nào tạo trùng.

**Tự kiểm:** A đã rollback nên còn 0 record; B đã commit nên còn 2 dù lần chạy
báo lỗi. Sửa B bằng protocol có key/version/upsert hoặc cơ chế stage/publish phù
hợp, rồi thử lại. Thêm case version cũ đến sau version mới để tránh upsert làm
lùi trạng thái. Checkpoint không được xác nhận batch khi target còn thiếu record.

**Nộp:** simulation, trạng thái sau lỗi/retry và 5 câu giải thích bằng tiếng Anh.
Nêu tại sao không thể suy từ SQLite transaction sang mọi Spark sink. Tuần 5 sẽ
chạy failure injection trên connector/sink thực; không khẳng định mọi write
của Spark đều partial hoặc đều atomic.

## Ngày 7 — Review và sửa điểm yếu

120 phút: 30 phút quiz độc lập; 45 phút sửa lỗi yếu nhất; 30 phút chạy lại tests
và review evidence; 15 phút learning log/PR. Quiz dùng fixture mới, không chép
lại output của ngày 1. Nếu cần, dùng chính buổi này hoàn thiện phần bài làm
chưa có evidence, không làm lại toàn bộ assessment 120 phút.

| Cửa kiểm tra | Điều kiện đạt |
|---|---|
| Grain/version | Giải thích grain và query chọn version; duplicate không thay metric |
| Incremental | Full = A→B = A→B→B; late event/correction không bị mất |
| SCD2 | Boundary đúng, phát hiện overlap/gap và không fan-out fact |
| Python | JSON/contract errors được tách, valid/quarantine có tests |
| Streaming | Không đọc/giữ toàn file; có evidence laziness và số đo được diễn giải đúng |
| Failure/retry | Tái hiện committed data còn lại sau failed run; replay đúng, không downgrade version |

Đánh dấu đạt bằng file/command/output, không tự cộng điểm chỉ vì đã đọc tài
liệu. Nếu thiếu cửa, ghi cụ thể và sửa trước khi mở rộng thành phần phụ thuộc.
Nếu cần kéo dài, giữ 2 giờ/ngày và báo tiến độ thật; không coi quiz bằng lời
thay cho code/tests chưa chạy.

## Evidence, cập nhật và xử lý lỗi

Lưu `docs/learning/evidence/week01.md`: ngày/buổi, commit, command, expected/
actual, giả định, phần AI hỗ trợ, điều tự sửa và câu hỏi còn mở. Commit code,
fixture nhỏ, tests, tài liệu; không commit database, dataset lớn hay secrets.
Thực hiện PR theo `AGENTS.md`; người học giải thích diff trước khi merge.

- Không tìm thấy `python3`: cài interpreter theo hướng dẫn OS ở trên rồi kiểm
  tra lại version; không cần chỉnh global alias hoặc Python hệ thống.
- Lỗi gần `OVER`: kiểm tra SQLite thực sự được interpreter đang chạy dùng;
  nâng interpreter phù hợp nếu SQLite dưới 3.25, không sửa query để bỏ window.
- Không có bảng: fixture dùng database RAM; chạy cả setup và query trong cùng
  process/connection, không mở connection mới rồi kỳ vọng dữ liệu còn đó.
- Cập nhật bài học từ Git chỉ khi đã lưu thay đổi cá nhân; review diff trước khi
  đưa vào nhánh bài làm. Không overwrite lời giải của mình bằng fixture mới.
- Không có dịch vụ cần gỡ ở tuần 1. Xóa script/output thử nghiệm chỉ khi đã lưu
  phần cần giữ; không xóa cả checkout hoặc gỡ Python mà project khác đang dùng.

## Nguồn đọc theo ngày

- Ngày 1–3: [SQLite window functions](https://www.sqlite.org/windowfunctions.html),
  [Kimball SCD Type 2](https://www.kimballgroup.com/2008/09/slowly-changing-dimensions-part-2/).
- Ngày 4: [Python json](https://docs.python.org/3/library/json.html),
  [datetime](https://docs.python.org/3/library/datetime.html),
  [unittest](https://docs.python.org/3/library/unittest.html).
- Ngày 5: [Python generators](https://docs.python.org/3/tutorial/classes.html#generators),
  [tracemalloc](https://docs.python.org/3/library/tracemalloc.html).
- Ngày 6: [Python sqlite3 transaction control](https://docs.python.org/3/library/sqlite3.html#transaction-control),
  [Spark JDBC data source](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html).

Đọc đoạn liên quan trong 20 phút, tra version của interpreter/connector mình
dùng. Không yêu cầu đọc hết tài liệu trước khi thử bài.
