import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_slide_layout = prs.slide_layouts[6]
    
    # Color Palette: Deep Navy, Modern Teal, Accent Coral, Card Dark, White
    COLOR_BG = RGBColor(15, 23, 42)        # #0F172A (Slate 900)
    COLOR_CARD = RGBColor(30, 41, 59)      # #1E293B (Slate 800)
    COLOR_PRIMARY = RGBColor(14, 165, 233)  # #0EA5E9 (Sky Blue)
    COLOR_ACCENT = RGBColor(244, 63, 94)    # #F43F5E (Rose Accent)
    COLOR_TEXT = RGBColor(241, 245, 249)    # #F1F5F9 (Light Grey/White)
    COLOR_MUTED = RGBColor(148, 163, 184)   # #94A3B8 (Slate Muted)
    COLOR_HIGHLIGHT = RGBColor(16, 185, 129)# #10B981 (Emerald Green)

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="MARKMATE ATTENDANCE SYSTEM"):
        # Category label
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_PRIMARY
        p_cat.font.name = "Calibri"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT
        p_title.font.name = "Calibri"

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = COLOR_CARD
        return shape

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide1, COLOR_BG)

    # Decorative hero card background
    add_card(slide1, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1), bg_color=COLOR_CARD)
    
    # Title Box
    tbox = slide1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "MARKMATE"
    p0.font.size = Pt(44)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_PRIMARY
    p0.font.name = "Calibri"
    
    p1 = tf.add_paragraph()
    p1.text = "Modern Student Attendance Management System"
    p1.font.size = Pt(26)
    p1.font.color.rgb = COLOR_TEXT
    p1.font.bold = True
    p1.font.name = "Calibri"
    
    p2 = tf.add_paragraph()
    p2.text = "A sleek, automated full-stack web application designed for academic institution attendance tracking & record management."
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_before = Pt(14)
    p2.font.name = "Calibri"

    # Presenter Details Card
    tbox_info = slide1.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10.3), Inches(1.2))
    tf_info = tbox_info.text_frame
    p_info = tf_info.paragraphs[0]
    p_info.text = "Tech Stack: Python Flask • SQLAlchemy • MySQL / SQLite • Bootstrap 5"
    p_info.font.size = Pt(14)
    p_info.font.bold = True
    p_info.font.color.rgb = COLOR_HIGHLIGHT
    p_info.font.name = "Calibri"

    # ==========================================
    # SLIDE 2: Problem Statement & Solution
    # ==========================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide2, COLOR_BG)
    add_header(slide2, "Problem Statement & Solution")

    # Left Card - The Problem
    add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_p = slide2.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    
    p = tf_p.paragraphs[0]
    p.text = "❌ Traditional Challenges"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    points_p = [
        "Manual Roll Calls: Time-consuming and takes away valuable lecture time.",
        "Human Errors: High risk of miscalculated attendance totals and lost paper registers.",
        "Lack of Real-time Visibility: Students and faculty lack instant access to daily presence logs.",
        "Audit Difficulties: Searching historical records for specific dates or students is tedious."
    ]
    for pt in points_p:
        p_sub = tf_p.add_paragraph()
        p_sub.text = "• " + pt
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = COLOR_TEXT
        p_sub.space_before = Pt(10)

    # Right Card - The MarkMate Solution
    add_card(slide2, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0))
    tb_s = slide2.shapes.add_textbox(Inches(7.2), Inches(2.1), Inches(5.0), Inches(4.4))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    
    p = tf_s.paragraphs[0]
    p.text = "💡 The MarkMate Solution"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_HIGHLIGHT
    
    points_s = [
        "1-Click Attendance Marking: Instant interactive radio toggles for fast classroom logging.",
        "Centralized Dashboard: Live visual metric counters for Total, Present, and Absent counts.",
        "Duplicate Prevention: Automated database checks prevent double-marking for the same date.",
        "Search & Filtering: Filter historical attendance records by student name, roll number, or date."
    ]
    for pt in points_s:
        p_sub = tf_s.add_paragraph()
        p_sub.text = "• " + pt
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = COLOR_TEXT
        p_sub.space_before = Pt(10)

    # ==========================================
    # SLIDE 3: Key Features & Capabilities
    # ==========================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide3, COLOR_BG)
    add_header(slide3, "Key Features & Capabilities")

    features = [
        ("🔒 Admin Authentication", "Secure login system powered by Werkzeug password hashing session management to safeguard administrative operations."),
        ("📊 Analytics Dashboard", "Real-time summary metric cards displaying Total Enrolled Students, Present Today, Absent Today, and latest activity logs."),
        ("👨‍🎓 Student Management", "Complete CRUD operations: Add new students, edit profiles, search records, and delete with modal confirmation."),
        ("📝 Smart Attendance Marking", "Auto-loads active students with smart date selection and radio buttons for seamless Present / Absent marking."),
        ("🔍 Filterable Attendance Logs", "Comprehensive historical records table with status badges (Green/Red) and multi-parameter filters."),
        ("⚡ Dual Database Architecture", "Designed to run seamlessly on production MySQL or instant zero-config fallback on SQLite.")
    ]

    coords = [
        (Inches(0.8), Inches(1.8)), (Inches(4.8), Inches(1.8)), (Inches(8.8), Inches(1.8)),
        (Inches(0.8), Inches(4.5)), (Inches(4.8), Inches(4.5)), (Inches(8.8), Inches(4.5))
    ]

    for idx, (title, desc) in enumerate(features):
        x, y = coords[idx]
        add_card(slide3, x, y, Inches(3.7), Inches(2.4))
        tb = slide3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT
        p2.space_before = Pt(8)

    # ==========================================
    # SLIDE 4: Technology Architecture
    # ==========================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide4, COLOR_BG)
    add_header(slide4, "Technology Architecture & Stack")

    tech_stack = [
        ("Backend Framework", "Python 3 & Flask", "Flask Blueprints for modular route segregation & clean MVC architecture.", COLOR_PRIMARY),
        ("Database & ORM", "SQLAlchemy & MySQL / SQLite", "SQLAlchemy ORM for database abstraction, schema migrations, and relational integrity.", COLOR_HIGHLIGHT),
        ("Frontend & Styling", "HTML5, CSS3, Bootstrap 5", "Modern, responsive UI with customized dark-themed CSS and Bootstrap Icons.", COLOR_ACCENT),
        ("Security & Auth", "Werkzeug Security & Sessions", "Cryptographic password hashing and protected endpoint route decorators.", COLOR_PRIMARY)
    ]

    for idx, (layer, title, desc, color) in enumerate(tech_stack):
        y = Inches(1.8 + idx * 1.3)
        add_card(slide4, Inches(0.8), y, Inches(11.7), Inches(1.1))
        
        # Layer title left column
        tb_left = slide4.shapes.add_textbox(Inches(1.1), y + Inches(0.15), Inches(3.2), Inches(0.8))
        tf_l = tb_left.text_frame
        tf_l.word_wrap = True
        p_l = tf_l.paragraphs[0]
        p_l.text = layer.upper()
        p_l.font.size = Pt(11)
        p_l.font.bold = True
        p_l.font.color.rgb = color
        
        p_l2 = tf_l.add_paragraph()
        p_l2.text = title
        p_l2.font.size = Pt(16)
        p_l2.font.bold = True
        p_l2.font.color.rgb = COLOR_TEXT

        # Desc right column
        tb_right = slide4.shapes.add_textbox(Inches(4.5), y + Inches(0.25), Inches(7.7), Inches(0.7))
        tf_r = tb_right.text_frame
        tf_r.word_wrap = True
        p_r = tf_r.paragraphs[0]
        p_r.text = desc
        p_r.font.size = Pt(13)
        p_r.font.color.rgb = COLOR_MUTED

    # ==========================================
    # SLIDE 5: Database Design & Data Models
    # ==========================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide5, COLOR_BG)
    add_header(slide5, "Database Schema & Entity Models")

    models = [
        ("Admin Entity", "Table: `admins`", ["• id (Integer, Primary Key)", "• username (String, Unique)", "• password_hash (String)", "• created_at (DateTime)", "• set_password() / check_password()"], COLOR_PRIMARY),
        ("Student Entity", "Table: `students`", ["• id (Integer, Primary Key)", "• roll_number (String, Unique)", "• name (String, Not Null)", "• department (String)", "• semester (String)", "• attendance_records (1-to-Many)"], COLOR_HIGHLIGHT),
        ("Attendance Entity", "Table: `attendance`", ["• id (Integer, Primary Key)", "• student_id (Foreign Key -> students.id)", "• attendance_date (Date)", "• status ('Present' / 'Absent')", "• UniqueConstraint(student_id, date)"], COLOR_ACCENT)
    ]

    for idx, (m_name, m_table, m_fields, m_color) in enumerate(models):
        x = Inches(0.8 + idx * 4.0)
        add_card(slide5, x, Inches(1.8), Inches(3.7), Inches(5.0))
        
        tb = slide5.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = m_name
        p0.font.size = Pt(18)
        p0.font.bold = True
        p0.font.color.rgb = m_color
        
        p1 = tf.add_paragraph()
        p1.text = m_table
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_MUTED
        p1.space_before = Pt(4)
        
        p_space = tf.add_paragraph()
        p_space.text = "Schema Attributes:"
        p_space.font.size = Pt(13)
        p_space.font.bold = True
        p_space.font.color.rgb = COLOR_TEXT
        p_space.space_before = Pt(14)

        for field in m_fields:
            pf = tf.add_paragraph()
            pf.text = field
            pf.font.size = Pt(12)
            pf.font.color.rgb = COLOR_TEXT
            pf.space_before = Pt(6)

    # ==========================================
    # SLIDE 6: System Workflows & User Flow
    # ==========================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide6, COLOR_BG)
    add_header(slide6, "System Workflow & User Journey")

    workflows = [
        ("1. Authentication", "Admin logs into system using hashed credentials via Werkzeug protected auth endpoint."),
        ("2. Student Enrollment", "Faculty/Admin registers student profiles with unique Roll Numbers, Department & Semester."),
        ("3. Attendance Entry", "Select date, view full class roster, mark status via toggles, submit single bulk transaction."),
        ("4. Real-time Analysis", "Dashboard instantly recalculates statistics & attendance records log reflects new updates.")
    ]

    for idx, (w_title, w_desc) in enumerate(workflows):
        x = Inches(0.8 + idx * 3.0)
        add_card(slide6, x, Inches(2.2), Inches(2.7), Inches(4.4))
        
        tb = slide6.shapes.add_textbox(x + Inches(0.15), Inches(2.4), Inches(2.4), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = w_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        
        p2 = tf.add_paragraph()
        p2.text = w_desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_TEXT
        p2.space_before = Pt(16)

    # ==========================================
    # SLIDE 7: Future Scope & Roadmap
    # ==========================================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide7, COLOR_BG)
    add_header(slide7, "Future Enhancements & Roadmap")

    enhancements = [
        ("📁 Automated Export Reports", "Download daily/monthly attendance history into formatted CSV, Excel, or PDF reports for academic audits.", COLOR_PRIMARY),
        ("⚠️ Threshold & Low-Attendance Alerts", "Automatic warning flags & notifications for students dropping below mandatory thresholds (e.g. < 75%).", COLOR_ACCENT),
        ("📱 Student & Parent Portal", "Dedicated student dashboard view allowing individual self-check of attendance history & subject percentage.", COLOR_HIGHLIGHT),
        ("📸 Dynamic QR & AI Attendance", "Integration with facial recognition or dynamic QR codes projected in class for automated zero-contact attendance.", COLOR_PRIMARY)
    ]

    for idx, (title, desc, color) in enumerate(enhancements):
        x = Inches(0.8 if idx % 2 == 0 else 6.9)
        y = Inches(1.8 if idx < 2 else 4.5)
        
        add_card(slide7, x, y, Inches(5.6), Inches(2.4))
        tb = slide7.shapes.add_textbox(x + Inches(0.3), y + Inches(0.3), Inches(5.0), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_TEXT
        p2.space_before = Pt(10)

    # ==========================================
    # SLIDE 8: Conclusion & Q&A Slide
    # ==========================================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide8, COLOR_BG)

    add_card(slide8, Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5), bg_color=COLOR_CARD)
    
    tb_c = slide8.shapes.add_textbox(Inches(2.0), Inches(2.0), Inches(9.333), Inches(3.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    pc1 = tf_c.paragraphs[0]
    pc1.alignment = PP_ALIGN.CENTER
    pc1.text = "Thank You!"
    pc1.font.size = Pt(40)
    pc1.font.bold = True
    pc1.font.color.rgb = COLOR_PRIMARY
    
    pc2 = tf_c.add_paragraph()
    pc2.alignment = PP_ALIGN.CENTER
    pc2.text = "MarkMate - Automated Student Attendance Management System"
    pc2.font.size = Pt(20)
    pc2.font.bold = True
    pc2.font.color.rgb = COLOR_TEXT
    pc2.space_before = Pt(14)

    pc3 = tf_c.add_paragraph()
    pc3.alignment = PP_ALIGN.CENTER
    pc3.text = "Questions & Answers (Q&A)"
    pc3.font.size = Pt(24)
    pc3.font.bold = True
    pc3.font.color.rgb = COLOR_HIGHLIGHT
    pc3.space_before = Pt(24)

    # Save presentation
    output_path = "/Users/abhishekkumar/Desktop/Attendance/MarkMate_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
