class SVGGenerator:
    def __init__(self):
        self.colors = {
            "bg": "#282828",
            "fg": "#ebdbb2",
            "red": "#fb4934",
            "green": "#b8bb26",
            "yellow": "#fabd2f",
            "blue": "#83a598",
            "purple": "#d3869b",
            "aqua": "#8ec07c",
            "orange": "#fe8019",
            "gray": "#928374",
            "bg_dim": "#1d2021",
            "card_bg": "#282828",
            "border": "#3c3836"
        }
        self.width = 450
        self.font_family = "'Segoe UI', Ubuntu, Sans-Serif"

    def _get_header(self, width, height, title, icon_path=None):
        icon_svg = ""
        if icon_path:
            icon_svg = f'<path d="{icon_path}" fill="{self.colors["red"]}" transform="translate(25, 25) scale(1.2)"/>'
            
        return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .header {{ font: 600 18px {self.font_family}; fill: {self.colors['fg']}; }}
        .stat-label {{ font: 400 12px {self.font_family}; fill: {self.colors['gray']}; }}
        .stat-value {{ font: 700 20px {self.font_family}; fill: {self.colors['fg']}; }}
        .lang-name {{ font: 400 13px {self.font_family}; fill: {self.colors['fg']}; }}
        .lang-percent {{ font: 400 12px {self.font_family}; fill: {self.colors['gray']}; }}
        .bg {{ fill: {self.colors['card_bg']}; stroke: {self.colors['border']}; stroke-width: 1px; }}
    </style>
    <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="10" class="bg"/>
    <text x="25" y="35" class="header">{title}</text>
    <line x1="25" y1="50" x2="{width-25}" y2="50" stroke="{self.colors['border']}" stroke-width="1"/>
'''

    def generate_streak_svg(self, streak_data, total_contributions):
        height = 210
        svg = self._get_header(self.width, height, "Contribution Stats")
        
        # Icons
        # Flame for Streak
        flame_path = "M12 23a7.5 7.5 0 0 1-5.138-12.963C8.202 8.725 12 3.5 12 3.5s3.798 5.225 5.138 6.537A7.5 7.5 0 0 1 12 23Z"
        # Chart for Total
        chart_path = "M3 3v18h18v-2H5V3H3zm4 14h2v-4H7v4zm4 0h2V9h-2v8zm4 0h2V5h-2v12z"
        # Trophy for Longest
        trophy_path = "M6 2h12a1 1 0 0 1 1 1v3c0 3.3-2.4 6.1-5.5 6.8A5.5 5.5 0 0 1 10.5 15H10v3h4v2H6v-2h4v-3h-.5A5.5 5.5 0 0 1 4.5 9.8C1.4 9.1-1 6.3-1 3V3a1 1 0 0 1 1-1zm1 2v3c0 2.2 1.6 4 4 4s4-1.8 4-4V4H7zm-5 0v1c0 1.9 1.3 3.4 3 3.8V4H2zm18 0h-3v4.8c1.7-.4 3-1.9 3-3.8V4z"

        # Layout
        col_width = (self.width - 50) / 3
        
        # 1. Total Contributions
        x1 = 25 + col_width * 0.5
        svg += f'''
    <g transform="translate({x1}, 110)">
        <path d="{chart_path}" fill="{self.colors['blue']}" transform="translate(-12, -40) scale(1)"/>
        <text x="0" y="10" text-anchor="middle" class="stat-value">{total_contributions}</text>
        <text x="0" y="30" text-anchor="middle" class="stat-label">Total Contributions</text>
    </g>'''

        # 2. Current Streak
        x2 = 25 + col_width * 1.5
        svg += f'''
    <g transform="translate({x2}, 110)">
        <path d="{flame_path}" fill="{self.colors['orange']}" transform="translate(-12, -40) scale(1)"/>
        <text x="0" y="10" text-anchor="middle" class="stat-value">{streak_data['currentStreak']}</text>
        <text x="0" y="30" text-anchor="middle" class="stat-label">Current Streak</text>
    </g>'''

        # 3. Longest Streak
        x3 = 25 + col_width * 2.5
        svg += f'''
    <g transform="translate({x3}, 110)">
        <path d="{trophy_path}" fill="{self.colors['yellow']}" transform="translate(-12, -40) scale(1)"/>
        <text x="0" y="10" text-anchor="middle" class="stat-value">{streak_data['longestStreak']}</text>
        <text x="0" y="30" text-anchor="middle" class="stat-label">Longest Streak</text>
    </g>'''

        svg += "\n</svg>"
        return svg

    def generate_languages_svg(self, languages):
        # Calculate height based on number of languages
        # Header: 50px
        # Each row: 35px
        # Padding bottom: 15px
        num_langs = len(languages)
        height = 60 + (num_langs * 40) + 10
        
        svg = self._get_header(self.width, height, "Most Used Languages")
        
        y_offset = 80
        
        for lang in languages:
            name = lang['name']
            percent = lang['percentage']
            color = lang['color'] if lang['color'] else self.colors['fg']
            
            # Progress bar width
            bar_width = 250
            fill_width = (percent / 100) * bar_width
            
            svg += f'''
    <g transform="translate(25, {y_offset})">
        <text x="0" y="0" class="lang-name">{name}</text>
        <text x="{self.width - 50}" y="0" text-anchor="end" class="lang-percent">{percent:.1f}%</text>
        
        <!-- Progress Bar Background -->
        <rect x="0" y="8" width="{bar_width}" height="6" rx="3" fill="{self.colors['bg_dim']}"/>
        
        <!-- Progress Bar Fill -->
        <rect x="0" y="8" width="{fill_width}" height="6" rx="3" fill="{color}"/>
    </g>'''
            y_offset += 40
            
        svg += "\n</svg>"
        return svg
