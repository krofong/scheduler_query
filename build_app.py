import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/krofo/Desktop/claude/schedule_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)

html_template = r'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>課表查詢系統</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Microsoft JhengHei", "微軟正黑體", sans-serif; background: #f0f4f8; color: #333; }

.header {
  background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
  color: white; padding: 20px 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.header h1 { font-size: 24px; }
.header .subtitle { font-size: 14px; opacity: 0.8; margin-top: 4px; }

.container { max-width: 1200px; margin: 0 auto; padding: 20px; }

.tabs {
  display: flex; margin-bottom: 20px; background: white; border-radius: 10px;
  overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.tab {
  flex: 1; padding: 14px 20px; text-align: center; cursor: pointer;
  font-size: 16px; font-weight: 600; border: none; background: white; color: #666;
  transition: all 0.3s;
}
.tab:hover { background: #f0f7ff; color: #2d6a9f; }
.tab.active { background: #2d6a9f; color: white; }

.panel { display: none; }
.panel.active { display: block; }

.search-box {
  background: white; border-radius: 10px; padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;
}
.search-box h2 { font-size: 18px; margin-bottom: 16px; color: #1e3a5f; }
.search-box > p { color: #666; font-size: 14px; margin-bottom: 16px; }

.search-row {
  display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end;
}
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; color: #555; }
.field select, .field input {
  padding: 10px 14px; border: 2px solid #ddd; border-radius: 8px;
  font-size: 15px; min-width: 180px; font-family: inherit;
  transition: border-color 0.3s;
}
.field select:focus, .field input:focus { border-color: #2d6a9f; outline: none; }

.btn {
  padding: 10px 28px; border: none; border-radius: 8px; font-size: 15px;
  font-weight: 600; cursor: pointer; transition: all 0.3s; font-family: inherit;
}
.btn-primary { background: #2d6a9f; color: white; }
.btn-primary:hover { background: #1e3a5f; }

.schedule-grid {
  background: white; border-radius: 10px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;
}
.schedule-grid table { width: 100%; border-collapse: collapse; }
.schedule-grid th {
  background: #1e3a5f; color: white; padding: 12px 8px;
  font-size: 14px; text-align: center;
}
.schedule-grid td {
  border: 1px solid #e0e0e0; padding: 8px; text-align: center;
  font-size: 13px; vertical-align: top; height: 70px;
}
.schedule-grid tr:nth-child(even) td { background: #f8fafc; }
.schedule-grid .period-col {
  background: #eef3f9; font-weight: 600; width: 100px; color: #1e3a5f;
}
.cell-subject { font-weight: 600; color: #1e3a5f; }
.cell-teacher { font-size: 12px; color: #666; margin-top: 2px; }
.cell-room { font-size: 11px; color: #999; margin-top: 2px; }
.cell-empty { color: #ccc; }

.info-cards {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px; margin-bottom: 20px;
}
.info-card {
  background: white; border-radius: 10px; padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.info-card h3 { color: #1e3a5f; margin-bottom: 10px; font-size: 16px; }
.info-card p { color: #555; font-size: 14px; line-height: 1.6; }
.info-card .value { font-size: 24px; font-weight: 700; color: #2d6a9f; }

.sub-result {
  background: white; border-radius: 10px; padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.sub-result h3 { color: #1e3a5f; margin-bottom: 16px; }

.candidate-list { list-style: none; }
.candidate-item {
  display: flex; align-items: center; padding: 12px 16px;
  border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 8px;
  transition: all 0.3s;
}
.candidate-item:hover { background: #f0f7ff; border-color: #2d6a9f; }
.candidate-rank {
  width: 32px; height: 32px; border-radius: 50%; display: flex;
  align-items: center; justify-content: center; font-weight: 700;
  font-size: 14px; margin-right: 14px; flex-shrink: 0;
}
.rank-primary { background: #2d6a9f; color: white; }
.rank-secondary { background: #f0a030; color: white; }
.candidate-info { flex: 1; }
.candidate-name { font-weight: 600; font-size: 15px; }
.candidate-dept { font-size: 13px; color: #888; margin-top: 4px; }
.candidate-tag {
  padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
}
.tag-same-dept { background: #e6f4ea; color: #1a7f37; }
.tag-same-group { background: #fff3e0; color: #e65100; }

.no-match { text-align: center; padding: 40px; color: #888; }
.no-match .msg { font-size: 16px; margin-bottom: 8px; font-weight: 600; }
.no-match .hint { font-size: 14px; color: #aaa; }

.alert-box {
  background: #fff3e0; border: 1px solid #ffcc80; border-radius: 8px;
  padding: 14px 18px; margin-top: 16px; color: #e65100; font-size: 14px;
}

.period-times { font-size: 11px; color: #888; font-weight: normal; }

.autocomplete-wrapper { position: relative; }
.autocomplete-list {
  position: absolute; top: 100%; left: 0; right: 0; background: white;
  border: 1px solid #ddd; border-top: none; border-radius: 0 0 8px 8px;
  max-height: 200px; overflow-y: auto; z-index: 100; display: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.autocomplete-list div { padding: 8px 14px; cursor: pointer; font-size: 14px; }
.autocomplete-list div:hover { background: #f0f7ff; }

.homeroom-badge {
  display: inline-block; background: #e8f5e9; color: #2e7d32;
  padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-left: 8px;
}

.section-title {
  margin: 20px 0 12px; padding-left: 12px;
  border-left: 4px solid #2d6a9f; font-size: 16px; color: #1e3a5f;
}
.section-title.secondary { border-left-color: #f0a030; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>課表查詢與代課建議系統</h1>
    <div class="subtitle">114學年度 第2學期</div>
  </div>
</div>

<div class="container">
  <div class="tabs">
    <div class="tab active" onclick="switchTab('teacher')">教師課表查詢</div>
    <div class="tab" onclick="switchTab('class')">班級課表查詢</div>
    <div class="tab" onclick="switchTab('substitute')">代課教師建議</div>
  </div>

  <div id="panel-teacher" class="panel active">
    <div class="search-box">
      <h2>教師課表查詢</h2>
      <div class="search-row">
        <div class="field">
          <label>科別篩選</label>
          <select id="dept-filter" onchange="filterTeachers()">
            <option value="">全部科別</option>
          </select>
        </div>
        <div class="field">
          <label>教師姓名</label>
          <div class="autocomplete-wrapper">
            <input id="teacher-input" type="text" placeholder="輸入教師姓名..." oninput="showSuggestions('teacher')" onfocus="showSuggestions('teacher')">
            <div id="teacher-suggestions" class="autocomplete-list"></div>
          </div>
        </div>
        <button class="btn btn-primary" onclick="searchTeacher()">查詢</button>
      </div>
    </div>
    <div id="teacher-result"></div>
  </div>

  <div id="panel-class" class="panel">
    <div class="search-box">
      <h2>班級課表查詢</h2>
      <div class="search-row">
        <div class="field">
          <label>年級篩選</label>
          <select id="grade-filter" onchange="filterClasses()">
            <option value="">全部年級</option>
            <option value="一">一年級</option>
            <option value="二">二年級</option>
            <option value="三">三年級</option>
          </select>
        </div>
        <div class="field">
          <label>班級名稱</label>
          <div class="autocomplete-wrapper">
            <input id="class-input" type="text" placeholder="輸入班級名稱..." oninput="showSuggestions('class')" onfocus="showSuggestions('class')">
            <div id="class-suggestions" class="autocomplete-list"></div>
          </div>
        </div>
        <button class="btn btn-primary" onclick="searchClass()">查詢</button>
      </div>
    </div>
    <div id="class-result"></div>
  </div>

  <div id="panel-substitute" class="panel">
    <div class="search-box">
      <h2>代課教師建議查詢</h2>
      <p>請選擇需要代課的教師、星期與節次，系統將根據代課原則推薦適合的代課人選。</p>
      <div class="search-row">
        <div class="field">
          <label>請假教師</label>
          <div class="autocomplete-wrapper">
            <input id="sub-teacher-input" type="text" placeholder="輸入教師姓名..." oninput="showSuggestions('sub-teacher')" onfocus="showSuggestions('sub-teacher')">
            <div id="sub-teacher-suggestions" class="autocomplete-list"></div>
          </div>
        </div>
        <div class="field">
          <label>星期</label>
          <select id="sub-day">
            <option value="1">星期一</option>
            <option value="2">星期二</option>
            <option value="3">星期三</option>
            <option value="4">星期四</option>
            <option value="5">星期五</option>
          </select>
        </div>
        <div class="field">
          <label>節次</label>
          <select id="sub-period">
            <option value="1">第1節</option>
            <option value="2">第2節</option>
            <option value="3">第3節</option>
            <option value="4">第4節</option>
            <option value="5">第5節</option>
            <option value="6">第6節</option>
            <option value="7">第7節</option>
            <option value="8">第8節</option>
          </select>
        </div>
        <button class="btn btn-primary" onclick="searchSubstitute()">查詢建議</button>
      </div>
    </div>
    <div id="sub-result"></div>
  </div>
</div>

<script>
const DATA = __JSON_DATA__;

const PERIOD_TIMES = {
  1:"08:10-09:00", 2:"09:10-10:00", 3:"10:10-11:00", 4:"11:10-12:00",
  5:"13:20-14:10", 6:"14:20-15:10", 7:"15:20-16:10", 8:"16:20-17:10",
  12:"12:30-13:20"
};

const DEPT_GROUPS = {
  "設計群": ["美廣科", "室設科"],
  "土木建築群": ["土建科"],
  "商管群": ["商科", "資料科"],
  "電機電子群": ["電資科"],
  "語文群": ["國文科", "本土語"],
  "社會群": ["社會科"],
  "自然群": ["自然科"],
  "數學群": ["數學科"],
  "英文群": ["英文科"],
  "體育群": ["體育科"],
  "藝術群": ["音樂科"],
  "健護群": ["健護"],
  "國防群": ["全民國防"]
};

const DEPT_TO_GROUP = {};
for (const [group, depts] of Object.entries(DEPT_GROUPS)) {
  for (const d of depts) DEPT_TO_GROUP[d] = group;
}

const teacherBusy = {};
for (const d of DATA.teacherSchedule) {
  if (!teacherBusy[d.teacher]) teacherBusy[d.teacher] = {};
  teacherBusy[d.teacher][d.day + "-" + d.period] = { subject: d.subject, "class": d["class"], room: d.room };
}

const allTeachers = [...new Set(DATA.teacherSchedule.map(d => d.teacher))].sort();
const allClasses = [...new Set(DATA.classSchedule.map(d => d["class"]))].sort();
const allDepts = [...new Set(Object.values(DATA.teacherDept))].sort();

// Populate dept filter
const deptFilter = document.getElementById("dept-filter");
allDepts.forEach(d => {
  const opt = document.createElement("option");
  opt.value = d; opt.textContent = d;
  deptFilter.appendChild(opt);
});

let currentTeachers = allTeachers;

function switchTab(tab) {
  document.querySelectorAll(".tab").forEach((t, i) => {
    t.classList.toggle("active", ["teacher","class","substitute"][i] === tab);
  });
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.getElementById("panel-" + tab).classList.add("active");
}

function filterTeachers() {
  const dept = document.getElementById("dept-filter").value;
  currentTeachers = dept ? allTeachers.filter(t => DATA.teacherDept[t] === dept) : allTeachers;
  document.getElementById("teacher-input").value = "";
}

function filterClasses() {
  document.getElementById("class-input").value = "";
  showSuggestions("class");
}

function showSuggestions(type) {
  let input, list, items;
  if (type === "teacher") {
    input = document.getElementById("teacher-input");
    list = document.getElementById("teacher-suggestions");
    const val = input.value.trim();
    items = currentTeachers.filter(t => !val || t.includes(val)).slice(0, 15);
    if (!val && items.length > 15) { list.style.display = "none"; return; }
    list.innerHTML = items.map(t => {
      const dept = DATA.teacherDept[t] || "";
      return "<div onclick=\"selectItem('teacher','" + t + "')\">" + t + " <span style='color:#999;font-size:12px'>(" + dept + ")</span></div>";
    }).join("");
  } else if (type === "class") {
    input = document.getElementById("class-input");
    list = document.getElementById("class-suggestions");
    const val = input.value.trim();
    const grade = document.getElementById("grade-filter").value;
    let filtered = allClasses;
    if (grade) filtered = filtered.filter(c => c.includes(grade));
    items = filtered.filter(c => !val || c.includes(val)).slice(0, 20);
    if (!val && !grade) { list.style.display = "none"; return; }
    list.innerHTML = items.map(c =>
      "<div onclick=\"selectItem('class','" + c + "')\">" + c + "</div>"
    ).join("");
  } else if (type === "sub-teacher") {
    input = document.getElementById("sub-teacher-input");
    list = document.getElementById("sub-teacher-suggestions");
    const val = input.value.trim();
    if (!val) { list.style.display = "none"; return; }
    items = allTeachers.filter(t => t.includes(val)).slice(0, 15);
    list.innerHTML = items.map(t => {
      const dept = DATA.teacherDept[t] || "";
      return "<div onclick=\"selectItem('sub-teacher','" + t + "')\">" + t + " <span style='color:#999;font-size:12px'>(" + dept + ")</span></div>";
    }).join("");
  }
  list.style.display = items.length ? "block" : "none";
}

function selectItem(type, name) {
  if (type === "teacher") {
    document.getElementById("teacher-input").value = name;
    document.getElementById("teacher-suggestions").style.display = "none";
    searchTeacher();
  } else if (type === "class") {
    document.getElementById("class-input").value = name;
    document.getElementById("class-suggestions").style.display = "none";
    searchClass();
  } else if (type === "sub-teacher") {
    document.getElementById("sub-teacher-input").value = name;
    document.getElementById("sub-teacher-suggestions").style.display = "none";
  }
}

document.addEventListener("click", e => {
  document.querySelectorAll(".autocomplete-list").forEach(list => {
    if (!list.parentElement.contains(e.target)) list.style.display = "none";
  });
});

function buildScheduleGrid(data, isTeacher) {
  const grid = {};
  const periods = new Set();
  for (const d of data) {
    const key = d.day + "-" + d.period;
    if (!grid[key]) grid[key] = [];
    grid[key].push(d);
    periods.add(d.period);
  }
  const sortedPeriods = [...periods].sort((a, b) => a - b);
  const days = [1, 2, 3, 4, 5];
  const dayNames = ["一", "二", "三", "四", "五"];

  let html = '<div class="schedule-grid"><table><thead><tr>';
  html += '<th style="width:100px">節次</th>';
  dayNames.forEach(d => html += "<th>星期" + d + "</th>");
  html += "</tr></thead><tbody>";

  for (const p of sortedPeriods) {
    html += "<tr>";
    html += '<td class="period-col">第' + p + '節<br><span class="period-times">' + (PERIOD_TIMES[p] || "") + "</span></td>";
    for (const day of days) {
      const cells = grid[day + "-" + p];
      if (cells && cells.length) {
        html += "<td>";
        for (const cell of cells) {
          const subj = cell.subject || "";
          const info = isTeacher ? (cell["class"] || "") : (cell.teacher || "");
          const room = cell.room || "";
          html += '<div class="cell-subject">' + subj + "</div>";
          if (info) html += '<div class="cell-teacher">' + info + "</div>";
          if (room) html += '<div class="cell-room">' + room + "</div>";
        }
        html += "</td>";
      } else {
        html += '<td class="cell-empty">&mdash;</td>';
      }
    }
    html += "</tr>";
  }
  html += "</tbody></table></div>";
  return html;
}

function searchTeacher() {
  const name = document.getElementById("teacher-input").value.trim();
  const result = document.getElementById("teacher-result");
  if (!name) { result.innerHTML = ""; return; }

  const schedule = DATA.teacherSchedule.filter(d => d.teacher === name);
  if (!schedule.length) {
    result.innerHTML = '<div class="no-match"><div class="msg">找不到教師「' + name + '」的課表資料</div></div>';
    return;
  }

  const dept = DATA.teacherDept[name] || "未知";
  const subjects = [...new Set(schedule.map(d => d.subject))].join("、");
  const classes = [...new Set(schedule.map(d => d["class"]).filter(Boolean))].join("、");

  let homeroomClass = "";
  for (const [cls, teacher] of Object.entries(DATA.homeroom)) {
    if (teacher === name) { homeroomClass = cls; break; }
  }

  let html = '<div class="info-cards">';
  html += '<div class="info-card"><h3>教師資訊</h3>';
  html += "<p><strong>" + name + "</strong>";
  if (homeroomClass) html += '<span class="homeroom-badge">導師：' + homeroomClass + "</span>";
  html += "</p><p>科別：" + dept + "</p>";
  html += '<p>授課節數：<span class="value">' + schedule.length + "</span> 節/週</p></div>";
  html += '<div class="info-card"><h3>授課科目</h3><p>' + subjects + "</p></div>";
  html += '<div class="info-card"><h3>授課班級</h3><p>' + classes + "</p></div>";
  html += "</div>";
  html += buildScheduleGrid(schedule, true);
  result.innerHTML = html;
}

function searchClass() {
  const name = document.getElementById("class-input").value.trim();
  const result = document.getElementById("class-result");
  if (!name) { result.innerHTML = ""; return; }

  const schedule = DATA.classSchedule.filter(d => d["class"] === name);
  if (!schedule.length) {
    result.innerHTML = '<div class="no-match"><div class="msg">找不到班級「' + name + '」的課表資料</div></div>';
    return;
  }

  const homeroom = DATA.homeroom[name] || "未設定";
  const subjects = [...new Set(schedule.map(d => d.subject))].join("、");

  let html = '<div class="info-cards">';
  html += '<div class="info-card"><h3>班級資訊</h3>';
  html += "<p><strong>" + name + "</strong></p>";
  html += "<p>導師：" + homeroom + "</p>";
  html += '<p>每週節數：<span class="value">' + schedule.length + "</span> 節</p></div>";
  html += '<div class="info-card"><h3>開設科目</h3><p>' + subjects + "</p></div>";
  html += "</div>";
  html += buildScheduleGrid(schedule, false);
  result.innerHTML = html;
}

function searchSubstitute() {
  const teacherName = document.getElementById("sub-teacher-input").value.trim();
  const day = parseInt(document.getElementById("sub-day").value);
  const period = parseInt(document.getElementById("sub-period").value);
  const result = document.getElementById("sub-result");

  if (!teacherName) {
    result.innerHTML = '<div class="alert-box">請輸入請假教師姓名</div>';
    return;
  }

  const slotKey = day + "-" + period;
  const absentSlot = (teacherBusy[teacherName] || {})[slotKey];
  const dayName = ["一","二","三","四","五"][day - 1];

  if (!absentSlot) {
    result.innerHTML = '<div class="alert-box">教師「' + teacherName + '」在星期' + dayName + '第' + period + '節沒有排課。</div>';
    return;
  }

  const absentDept = DATA.teacherDept[teacherName] || "";
  const absentGroup = DEPT_TO_GROUP[absentDept] || "";
  const absentSubject = absentSlot.subject;
  const targetClass = absentSlot["class"];

  const freeTeachers = allTeachers.filter(t => {
    if (t === teacherName) return false;
    return !(teacherBusy[t] || {})[slotKey];
  });

  const sameDeptSameSubject = [];
  const sameDept = [];
  const sameGroupSameSubject = [];
  const sameGroup = [];

  for (const t of freeTeachers) {
    const tDept = DATA.teacherDept[t] || "";
    const tGroup = DEPT_TO_GROUP[tDept] || "";
    const tSubjects = DATA.teacherSubjects[t] || [];
    const teachesSubject = tSubjects.includes(absentSubject);

    if (tDept === absentDept) {
      if (teachesSubject) sameDeptSameSubject.push(t);
      else sameDept.push(t);
    } else if (tGroup && tGroup === absentGroup && DEPT_GROUPS[tGroup] && DEPT_GROUPS[tGroup].length > 1) {
      if (teachesSubject) sameGroupSameSubject.push(t);
      else sameGroup.push(t);
    }
  }

  let html = '<div class="sub-result">';
  html += "<h3>代課建議結果</h3>";
  html += '<div class="info-cards" style="margin-bottom:20px">';
  html += '<div class="info-card"><h3>請假教師</h3><p><strong>' + teacherName + "</strong>（" + absentDept + "）</p></div>";
  html += '<div class="info-card"><h3>代課時段</h3><p>星期' + dayName + " 第" + period + "節 (" + (PERIOD_TIMES[period] || "") + ")</p></div>";
  html += '<div class="info-card"><h3>課程資訊</h3><p>科目：<strong>' + absentSubject + "</strong></p><p>班級：" + targetClass + "</p></div>";
  html += "</div>";

  const hasPrimary = sameDeptSameSubject.length > 0 || sameDept.length > 0;
  const hasSecondary = sameGroupSameSubject.length > 0 || sameGroup.length > 0;

  if (!hasPrimary && !hasSecondary) {
    html += '<div class="no-match">';
    html += '<div style="font-size:48px;margin-bottom:16px">&#9888;</div>';
    html += '<div class="msg">無法媒合代課教師</div>';
    html += '<div class="hint">該時段無同科或同科群教師有空堂，請洽教學組安排。</div>';
    html += "</div>";
  } else {
    if (hasPrimary) {
      html += '<div class="section-title">第一優先：同科代課（建議名單）</div>';
      html += '<ul class="candidate-list">';
      let rank = 1;
      for (const t of sameDeptSameSubject)
        html += buildCandidate(t, rank++, true, "同科+同科目");
      for (const t of sameDept)
        html += buildCandidate(t, rank++, true, "同科");
      html += "</ul>";
    }
    if (hasSecondary) {
      html += '<div class="section-title secondary">第二優先：同科群代課（候選名單）</div>';
      html += '<ul class="candidate-list">';
      let rank = 1;
      for (const t of sameGroupSameSubject)
        html += buildCandidate(t, rank++, false, "同科群+同科目");
      for (const t of sameGroup)
        html += buildCandidate(t, rank++, false, "同科群");
      html += "</ul>";
    }
    if (!hasPrimary) {
      html += '<div class="alert-box">同科內無空堂教師，以上為同科群候選名單。若不適合，請洽教學組。</div>';
    }
  }

  html += "</div>";
  result.innerHTML = html;
}

function buildCandidate(teacher, rank, isPrimary, tag) {
  const dept = DATA.teacherDept[teacher] || "";
  const subjects = (DATA.teacherSubjects[teacher] || []).join("、");
  let homeroom = "";
  for (const [cls, t] of Object.entries(DATA.homeroom)) {
    if (t === teacher) { homeroom = "（導師：" + cls + "）"; break; }
  }
  const rc = isPrimary ? "rank-primary" : "rank-secondary";
  const tc = isPrimary ? "tag-same-dept" : "tag-same-group";

  return '<li class="candidate-item">' +
    '<div class="candidate-rank ' + rc + '">' + rank + "</div>" +
    '<div class="candidate-info">' +
    '<div class="candidate-name">' + teacher + ' <span style="color:#999;font-size:13px">' + dept + homeroom + "</span></div>" +
    '<div class="candidate-dept">授課科目：' + subjects + "</div>" +
    "</div>" +
    '<span class="candidate-tag ' + tc + '">' + tag + "</span>" +
    "</li>";
}
</script>
</body>
</html>'''

html_content = html_template.replace('__JSON_DATA__', json_str)

with open('C:/Users/krofo/Desktop/claude/schedule_app.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Done! schedule_app.html created successfully.')
