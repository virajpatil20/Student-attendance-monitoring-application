import { useState } from "react";

import {
  LayoutDashboard,
  Users,
  ClipboardCheck,
  FileBarChart,
  Settings,
  Bell,
  Search,
  CalendarDays,
  ChevronDown,
  TrendingUp,
  UserCheck,
  UserX,
  GraduationCap,
  Clock,
  Download,
  Plus,
  MoreHorizontal,
  Menu,
  X,
  CheckCircle2,
  CircleX,
} from "lucide-react";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import "./App.css";

const students = [
  { id: "1001", name: "Aarav Sharma", department: "Computer Engineering", status: "Present" },
  { id: "1002", name: "Ananya Patel", department: "Computer Engineering", status: "Present" },
  { id: "1003", name: "Rohan Mehta", department: "Computer Engineering", status: "Absent" },
  { id: "1004", name: "Isha Desai", department: "Computer Engineering", status: "Present" },
  { id: "1005", name: "Kabir Shah", department: "Computer Engineering", status: "Late" },
];

const attendanceData = [
  { day: "Mon", attendance: 82 },
  { day: "Tue", attendance: 88 },
  { day: "Wed", attendance: 76 },
  { day: "Thu", attendance: 91 },
  { day: "Fri", attendance: 86 },
  { day: "Sat", attendance: 94 },
  { day: "Sun", attendance: 89 },
];

const navigation = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "Students", icon: Users },
  { name: "Attendance", icon: ClipboardCheck },
  { name: "Reports", icon: FileBarChart },
];

function App() {
  const [activePage, setActivePage] = useState("Overview");
  const [search, setSearch] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [studentList, setStudentList] = useState(students);

  const presentCount = studentList.filter(
    (s) => s.status === "Present"
  ).length;

  const absentCount = studentList.filter(
    (s) => s.status === "Absent"
  ).length;

  const filteredStudents = studentList.filter(
    (student) =>
      student.name.toLowerCase().includes(search.toLowerCase()) ||
      student.id.includes(search)
  );

  const toggleAttendance = (id) => {
    setStudentList((prev) =>
      prev.map((student) =>
        student.id === id
          ? {
              ...student,
              status:
                student.status === "Present" ? "Absent" : "Present",
            }
          : student
      )
    );
  };

  return (
    <div className="app-container">

      {/* SIDEBAR */}

      <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`}>

        <div className="brand">
          <div className="brand-icon">
            <GraduationCap size={25} />
          </div>

          <div>
            <h2>SmartAttend</h2>
            <span>Attendance Management</span>
          </div>

          <button
            className="mobile-close"
            onClick={() => setMenuOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <div className="nav-section">
          <p className="nav-heading">MENU</p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => {
                  setActivePage(item.name);
                  setMenuOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </div>

        <div className="sidebar-bottom">

          <div className="help-card">
            <div className="help-icon">?</div>
            <h4>Need assistance?</h4>
            <p>Contact your college administrator.</p>
            <button>Get Help</button>
          </div>

          <button
            className={`nav-item ${
              activePage === "Settings" ? "active" : ""
            }`}
            onClick={() => setActivePage("Settings")}
          >
            <Settings size={19} />
            <span>Settings</span>
          </button>

          <div className="profile">
            <div className="avatar">AD</div>
            <div className="profile-info">
              <strong>Administrator</strong>
              <span>College Admin</span>
            </div>
            <MoreHorizontal size={20} />
          </div>

        </div>
      </aside>

      {/* MAIN CONTENT */}

      <main className="main-content">

        {/* HEADER */}

        <header className="topbar">

          <button
            className="mobile-menu"
            onClick={() => setMenuOpen(true)}
          >
            <Menu size={22} />
          </button>

          <div className="breadcrumb">
            <span>Workspace</span>
            <span>/</span>
            <strong>{activePage}</strong>
          </div>

          <div className="topbar-right">

            <div className="search-box">
              <Search size={17} />

              <input
                placeholder="Search admission number..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />

              <kbd>⌘ K</kbd>
            </div>

            <button className="notification-btn">
              <Bell size={20} />
              <span></span>
            </button>

            <div className="date-display">
              <CalendarDays size={17} />
              <span>
                {new Date().toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </span>
            </div>

          </div>
        </header>

        {/* PAGE CONTENT */}

        <div className="page-content">

          {activePage === "Overview" && (
            <>

              <div className="welcome-section">
                <div>
                  <p className="eyebrow">COLLEGE MANAGEMENT</p>
                  <h1>Good morning, Administrator 👋</h1>
                  <p className="subtitle">
                    Here's what's happening with your college attendance today.
                  </p>
                </div>

                <button className="primary-btn">
                  <Download size={17} />
                  Export Report
                </button>
              </div>

              {/* STATISTICS */}

              <section className="stats-grid">

                <div className="stat-card">
                  <div className="stat-top">
                    <span>Total Students</span>
                    <div className="stat-icon blue">
                      <Users size={20} />
                    </div>
                  </div>

                  <h2>1,248</h2>

                  <div className="stat-footer">
                    <span className="positive">
                      <TrendingUp size={14} /> 8.2%
                    </span>
                    <span>vs last semester</span>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-top">
                    <span>Present Today</span>
                    <div className="stat-icon green">
                      <UserCheck size={20} />
                    </div>
                  </div>

                  <h2>1,086</h2>

                  <div className="stat-footer">
                    <span className="positive">87.0%</span>
                    <span>of total students</span>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-top">
                    <span>Absent Today</span>
                    <div className="stat-icon red">
                      <UserX size={20} />
                    </div>
                  </div>

                  <h2>162</h2>

                  <div className="stat-footer">
                    <span className="negative">13.0%</span>
                    <span>of total students</span>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-top">
                    <span>Overall Attendance</span>
                    <div className="stat-icon purple">
                      <ClipboardCheck size={20} />
                    </div>
                  </div>

                  <h2>87.4%</h2>

                  <div className="stat-footer">
                    <span className="positive">
                      <TrendingUp size={14} /> 2.4%
                    </span>
                    <span>this month</span>
                  </div>
                </div>

              </section>

              {/* CHART AND SUMMARY */}

              <section className="middle-grid">

                <div className="content-card chart-card">

                  <div className="card-heading">
                    <div>
                      <h3>Attendance Overview</h3>
                      <p>Weekly attendance performance</p>
                    </div>

                    <button className="filter-btn">
                      This Week <ChevronDown size={15} />
                    </button>
                  </div>

                  <div className="chart-container">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={attendanceData}>

                        <defs>
                          <linearGradient
                            id="attendanceGradient"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                          >
                            <stop
                              offset="0%"
                              stopColor="#5278F5"
                              stopOpacity={0.2}
                            />
                            <stop
                              offset="100%"
                              stopColor="#5278F5"
                              stopOpacity={0}
                            />
                          </linearGradient>
                        </defs>

                        <CartesianGrid
                          strokeDasharray="3 3"
                          vertical={false}
                          stroke="#EDF0F5"
                        />

                        <XAxis
                          dataKey="day"
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: "#9299A8", fontSize: 12 }}
                        />

                        <YAxis
                          domain={[0, 100]}
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: "#9299A8", fontSize: 12 }}
                          tickFormatter={(value) => `${value}%`}
                        />

                        <Tooltip
                          formatter={(value) => [`${value}%`, "Attendance"]}
                        />

                        <Area
                          type="monotone"
                          dataKey="attendance"
                          stroke="#5278F5"
                          strokeWidth={3}
                          fill="url(#attendanceGradient)"
                        />

                      </AreaChart>
                    </ResponsiveContainer>
                  </div>

                </div>

                <div className="content-card summary-card">

                  <div className="card-heading">
                    <div>
                      <h3>Today's Summary</h3>
                      <p>Attendance breakdown</p>
                    </div>
                  </div>

                  <div className="attendance-circle">
                    <div className="circle-inner">
                      <h2>87%</h2>
                      <span>Attendance</span>
                    </div>
                  </div>

                  <div className="summary-row">
                    <div>
                      <span className="legend-dot green-dot"></span>
                      Present
                    </div>
                    <strong>1,086</strong>
                  </div>

                  <div className="summary-row">
                    <div>
                      <span className="legend-dot red-dot"></span>
                      Absent
                    </div>
                    <strong>162</strong>
                  </div>

                </div>

              </section>

            </>
          )}

          {/* STUDENTS */}

          {activePage === "Students" && (
            <section className="content-card table-card">

              <div className="card-heading">
                <div>
                  <h3>Student Directory</h3>
                  <p>Search and manage students using admission numbers.</p>
                </div>

                <button className="primary-btn">
                  <Plus size={17} /> Add Student
                </button>
              </div>

              <StudentTable
                students={filteredStudents}
                toggleAttendance={toggleAttendance}
              />

            </section>
          )}

          {/* ATTENDANCE */}

          {activePage === "Attendance" && (
            <section className="content-card table-card">

              <div className="card-heading">
                <div>
                  <h3>Daily Attendance</h3>
                  <p>Manage today's student attendance.</p>
                </div>

                <span className="live-badge">
                  <span></span> Attendance Session
                </span>
              </div>

              <div className="attendance-controls">
                <input type="date" defaultValue={
                  new Date().toLocaleDateString("en-CA")
                } />

                <select defaultValue="Computer Engineering">
                  <option>Computer Engineering</option>
                  <option>Information Technology</option>
                  <option>Mechanical Engineering</option>
                </select>

              </div>

              <StudentTable
                students={filteredStudents}
                toggleAttendance={toggleAttendance}
              />

              <div className="attendance-footer">
                <span>{presentCount} Present · {absentCount} Absent</span>
                <button className="primary-btn">
                  <CheckCircle2 size={17} />
                  Save Attendance
                </button>
              </div>

            </section>
          )}

          {/* REPORTS */}

          {activePage === "Reports" && (
            <section className="content-card table-card">
              <div className="card-heading">
                <div>
                  <h3>Attendance Reports</h3>
                  <p>Generate and review attendance reports.</p>
                </div>
              </div>

              <div className="report-options">
                {["Daily Report", "Monthly Report", "Student-wise Report", "Subject-wise Report"].map(
                  (report) => (
                    <div className="report-option" key={report}>
                      <FileBarChart size={23} />
                      <h4>{report}</h4>
                      <p>View attendance statistics and records.</p>
                      <button>Generate Report →</button>
                    </div>
                  )
                )}
              </div>
            </section>
          )}

          {/* SETTINGS */}

          {activePage === "Settings" && (
            <section className="content-card table-card">
              <h3>Application Settings</h3>
              <p>Configure your SmartAttend workspace.</p>
            </section>
          )}

          <footer className="footer">
            <span>© 2026 SmartAttend. All rights reserved.</span>
            <span>College Attendance Management System</span>
          </footer>

        </div>
      </main>
    </div>
  );
}

function StudentTable({ students, toggleAttendance }) {

  return (
    <div className="table-wrapper">

      <table>
        <thead>
          <tr>
            <th>ADMISSION NO.</th>
            <th>STUDENT NAME</th>
            <th>DEPARTMENT</th>
            <th>STATUS</th>
            <th>ACTION</th>
          </tr>
        </thead>

        <tbody>

          {students.map((student) => (
            <tr key={student.id}>

              <td>
                <strong>{student.id}</strong>
              </td>

              <td>{student.name}</td>

              <td>{student.department}</td>

              <td>
                <span className={`status-badge ${student.status.toLowerCase()}`}>
                  {student.status}
                </span>
              </td>

              <td>
                <button
                  className="status-action"
                  onClick={() => toggleAttendance(student.id)}
                >
                  Change Status
                </button>
              </td>

            </tr>
          ))}

          {students.length === 0 && (
            <tr>
              <td colSpan="5" className="empty-state">
                No students found.
              </td>
            </tr>
          )}

        </tbody>
      </table>

    </div>
  );
}

export default App;