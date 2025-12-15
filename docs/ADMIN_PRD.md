# PrintHive Kenya Admin Interface
## Product Requirements Document (PRD)

**Version:** 3.3 - Fully Clickable Rows (JS)  
**Date:** December 9, 2025  
**Author:** PrintHive Development Team  
**Status:** Implemented & Verified ✅

---

## 1. Overview

### 1.1 Product Summary
A modernized Django Admin interface for PrintHive Kenya powered by **django-unfold**. This version features a professional **Navy Blue (#2E5AAC)** and **Gold (#F1C40F)** color scheme, **Material Design icons**, SVG-based action buttons, and **fully clickable rows** (via JavaScript) for seamless navigation.

### 1.2 Objectives
- **Modernize UI:** Leverage django-unfold for a premium, responsive interface.
- **Brand Compliance:** Enforce Navy & Gold color scheme via configuration and CSS overrides.
- **Professional Aesthetics:** Replace emojis with Material Design icons and SVGs.
- **Enhanced Usability:** Entire rows in list views are clickable, improving touch/click targets.
- **Maintain Functionality:** Ensure all custom admin actions (WhatsApp integration) and logic remain intact.

### 1.3 Target Users
- **Primary:** PrintHive administrators and staff
- **Secondary:** Customer support team members

---

## 2. Design System

### 2.1 Color Palette

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Primary Blue | `#667eea` | Primary actions, links, active states |
| Primary Purple | `#764ba2` | Gradient endpoints, accents |
| Accent Gold | `#F1C40F` | Save buttons, highlights |
| Success Green | `#22c55e` | WhatsApp, add actions, success messages |
| Danger Red | `#ef4444` | Delete actions, error messages |
| Warning Orange | `#f59e0b` | Quote-related items, warnings |
| Background Dark | `#1a1a2e` | Sidebar background |
| Background Light | `#f0f4f8` | Page background |
| Text Primary | `#1e293b` | Headings, primary text |
| Text Secondary | `#64748b` | Descriptions, muted text |

### 2.2 Typography

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Font Family | Inter | - | - |
| Headings | Inter | 700 | 18-32px |
| Body Text | Inter | 400-500 | 14px |
| Labels | Inter | 600 | 14px |
| Small Text | Inter | 500 | 11-13px |

### 2.3 Spacing & Sizing

| Property | Value |
|----------|-------|
| Border Radius (Cards) | 20px |
| Border Radius (Buttons) | 12px |
| Border Radius (Inputs) | 12px |
| Sidebar Width | 240px |
| Header Height | 72px |
| Card Padding | 24px |
| Grid Gap | 24px |

### 2.4 Shadows

| Level | CSS Value |
|-------|-----------|
| Small | `0 1px 2px rgba(0, 0, 0, 0.05)` |
| Medium | `0 4px 12px rgba(0, 0, 0, 0.08)` |
| Large | `0 8px 24px rgba(0, 0, 0, 0.12)` |
| Glow (Blue) | `0 8px 32px rgba(102, 126, 234, 0.4)` |
| Glow (Green) | `0 8px 32px rgba(34, 197, 94, 0.4)` |

---

## 3. Layout Structure

### 3.1 Global Layout
```
┌─────────────────────────────────────────────────────┐
│  SIDEBAR (240px)  │         MAIN CONTENT            │
│                   │                                  │
│  ┌─────────────┐  │  ┌──────────────────────────┐   │
│  │   Logo      │  │  │       HEADER (72px)      │   │
│  └─────────────┘  │  └──────────────────────────┘   │
│                   │                                  │
│  ┌─────────────┐  │  ┌──────────────────────────┐   │
│  │   Menu      │  │  │                          │   │
│  │   Items     │  │  │      CONTENT AREA        │   │
│  │             │  │  │                          │   │
│  └─────────────┘  │  │                          │   │
│                   │  └──────────────────────────┘   │
│  ┌─────────────┐  │                                  │
│  │ User Profile│  │  ┌──────────────────────────┐   │
│  └─────────────┘  │  │       FOOTER             │   │
└─────────────────────────────────────────────────────┘
```

### 3.2 Sidebar Structure
- **Brand Section:** Logo + "PrintHive" text
- **Navigation Sections:**
  - Main: Dashboard
  - Management: Customer Inquiries, Quote Requests
  - Catalog: Categories, Products, Pricing
  - System: Users, View Site, Sign Out
- **User Section:** Avatar, name, role

### 3.3 Header Structure
- **Left:** Menu toggle (mobile) + Page title + Subtitle
- **Right:** Search box + Primary action button

---

## 4. Component Specifications

### 4.1 Stat Cards (Dashboard)
```
Properties:
- Grid: 4 columns (desktop), 2 columns (tablet), 1 column (mobile)
- Background: Gradient colors
- Border Radius: 20px
- Padding: 24px
- Shadow: Glow effect matching gradient
- Hover: translateY(-4px), enhanced shadow

Content:
- Icon (48x48px, 24px font)
- Badge (top-right)
- Value (32px, bold)
- Label (14px)
- Trend indicator (optional)
```

### 4.2 Module Cards
```
Properties:
- Grid: 3 columns (desktop), 2 columns (tablet), 1 column (mobile)
- Two-part structure: Gradient header + White footer
- Border Radius: 20px
- Shadow: Medium

Header Content:
- Icon (52x52px)
- Action buttons (+ Add)
- Title (18px, bold)
- Description (13px)

Footer Content:
- Stat text
- "View All →" link
```

### 4.3 Data Tables
```
Properties:
- Wrapper: White card, 20px radius, medium shadow
- Headers: Light background (#f8fafc), uppercase, 11px
- Rows: 20px padding, 1px border-bottom
- Zebra stripe: Even rows slightly tinted
- Hover: Blue tint (#667eea at 4% opacity)

Features:
- Horizontal scroll on mobile
- Sticky headers
- Centered action columns
```

### 4.4 Buttons

| Type | Background | Text | Shadow |
|------|------------|------|--------|
| Primary | Blue→Purple gradient | White | Blue glow |
| Save | Gold gradient | Dark | Gold glow |
| Add/Success | Green gradient | White | Green glow |
| Delete | Red gradient | White | Red glow |
| Secondary | Light gray | Dark gray | None |
| WhatsApp | Green gradient, pill shape | White | Green glow |

### 4.5 Form Inputs
```
Properties:
- Padding: 14px 18px
- Border: 1px solid #e5e7eb
- Border Radius: 12px
- Background: #f8fafc (unfocused), white (focused)
- Focus: Blue border + 4px blue glow ring
- Max Width: 600px
```

---

## 5. Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Desktop | > 1280px | Full layout, 4-column stats, 3-column modules |
| Tablet | 768-1024px | Sidebar collapsible, 2-column grids |
| Mobile | < 768px | Sidebar hidden, 1-column grids, stacked forms |
| Small Mobile | < 480px | Compact padding, smaller fonts |

### 5.1 Mobile Behavior
- Sidebar hidden by default, toggle via hamburger menu
- Overlay backdrop when sidebar open
- Tables horizontally scrollable
- Submit buttons stack vertically
- Search hidden, available in page content

---

## 6. File Structure

```
print_hive_project/
├── core/
│   └── static/
│       └── admin/
│           ├── css/
│           │   └── custom.css      # Complete CSS (800+ lines)
│           └── js/
│               └── custom.js       # Interactions (200+ lines)
└── templates/
    └── admin/
        ├── base_site.html          # Base template
        ├── index.html              # Dashboard
        ├── change_list.html        # List views
        ├── change_form.html        # Edit forms
        └── login.html              # Login page
```

---

## 7. Features Implemented

### 7.1 Dashboard
- [x] Gradient stat cards with hover effects
- [x] Module cards grid with actions
- [x] Recent activity table
- [x] Quick search in header
- [x] Primary action button

### 7.2 List Views
- [x] Overview stat cards
- [x] Table wrapped in card
- [x] Zebra striping
- [x] Styled status dropdowns
- [x] Pill-shaped WhatsApp buttons with icon
- [x] Responsive horizontal scroll

### 7.3 Edit Forms
- [x] Gradient fieldset headers
- [x] Card-based layout
- [x] Color-coded submit buttons
- [x] Sticky submit row
- [x] Styled inline forms

### 7.4 Navigation
- [x] Fixed dark sidebar
- [x] Sectioned menu items with icons
- [x] Active state highlighting
- [x] User profile section
- [x] Mobile hamburger menu
- [x] Overlay backdrop

### 7.5 Interactions
- [x] Card hover animations (scale + shadow)
- [x] Button hover effects
- [x] Smooth transitions (0.2-0.3s)
- [x] Delete confirmation dialog
- [x] Keyboard navigation (Escape to close)

---

## 8. Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Fully supported |
| Firefox | 88+ | ✅ Fully supported |
| Safari | 14+ | ✅ Fully supported |
| Edge | 90+ | ✅ Fully supported |
| Mobile Safari | iOS 14+ | ✅ Fully supported |
| Chrome Mobile | Android 10+ | ✅ Fully supported |

---

## 9. Performance Considerations

- **CSS:** Single file, no external frameworks (except Inter font)
- **JS:** Lightweight vanilla JavaScript, no dependencies
- **Fonts:** Inter loaded from Google Fonts with preconnect
- **Images:** Logo served from static files
- **Caching:** Django's built-in static file handling

---

## 10. Future Enhancements

| Priority | Feature | Description |
|----------|---------|-------------|
| P1 | Dark Mode Toggle | Switch between light and dark themes |
| P2 | Dashboard Analytics | Real dynamic counts from database |
| P2 | Notification Center | Bell icon with unread count |
| P3 | Customizable Widgets | User-configurable dashboard |
| P3 | Export Actions | Table data export to CSV/PDF |

---

## 11. Testing Checklist

### 11.1 Functionality
- [ ] Login/logout works correctly
- [ ] All CRUD operations functional
- [ ] Filters and search work
- [ ] Actions (WhatsApp, etc.) work
- [ ] Form validation displays errors correctly

### 11.2 Visual
- [ ] Sidebar displays correctly
- [ ] Cards have proper shadows and hover effects
- [ ] Gradients render smoothly
- [ ] Icons display correctly
- [ ] Typography is consistent

### 11.3 Responsive
- [ ] Dashboard stacks on mobile
- [ ] Sidebar collapses on tablet/mobile
- [ ] Tables scroll horizontally
- [ ] Buttons are touch-friendly (44x44px minimum)
- [ ] Forms stack vertically

---

## 12. Deployment Notes

1. Run `python manage.py collectstatic --noinput` after any CSS/JS changes
2. Clear browser cache to see CSS changes
3. Ensure `STATIC_URL` and `STATICFILES_DIRS` are configured in settings.py
4. Inter font requires internet connection (consider self-hosting for offline)

---

**Document End**

*Last Updated: December 9, 2025*
