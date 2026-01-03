import html

class SVGGenerator:
    COLORS = {
        "bg": "#282828",
        "fg": "#ebdbb2",
        "border": "#3c3836",
        "green": "#b8bb26",
        "yellow": "#fabd2f",
        "blue": "#83a598",
        "red": "#fb4934",
        "gray": "#928374",
        "purple": "#d3869b",
        "aqua": "#8ec07c",
        "orange": "#fe8019"
    }

    def __init__(self):
        pass

    def _get_style(self):
        return f"""
            <style>
                .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {self.COLORS['green']}; }}
                .stat {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {self.COLORS['fg']}; }}
                .stagger {{ animation: fadeInAnimation 0.8s ease-in-out forwards; }}
                @keyframes fadeInAnimation {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
            </style>
        """

    def generate_streak_svg(self, streak, total_contributions):
        width = 400
        height = 150
        
        svg = f"""
        <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="{width}" height="{height}" rx="4.5" fill="{self.COLORS['bg']}" stroke="{self.COLORS['border']}" />
            {self._get_style()}
            
            <g transform="translate(25, 35)">
                <text x="0" y="0" class="header">GitHub Streak</text>
            </g>
            
            <g transform="translate(25, 80)">
                <text x="0" y="0" class="stat" style="font-size: 32px; fill: {self.COLORS['fg']}">{streak}</text>
                <text x="0" y="25" class="stat" style="font-size: 12px; fill: {self.COLORS['gray']}">Current Streak (Days)</text>
            </g>
            
            <g transform="translate(200, 80)">
                <text x="0" y="0" class="stat" style="font-size: 32px; fill: {self.COLORS['fg']}">{total_contributions}</text>
                <text x="0" y="25" class="stat" style="font-size: 12px; fill: {self.COLORS['gray']}">Total Contributions</text>
            </g>
        </svg>
        """
        return svg

    def generate_languages_svg(self, languages):
        width = 350
        # Dynamic height based on number of languages, but let's fix it for now or make it flexible
        height = 200 
        
        bars_svg = ""
        y_offset = 55
        
        for i, lang in enumerate(languages):
            name = lang['name']
            percent = lang['percentage']
            color = lang['color'] if lang['color'] else self.COLORS['fg']
            
            # Ensure color is visible on dark bg, maybe adjust if needed, but usually GitHub colors are okay.
            # Gruvbox override? No, keep language colors for recognition, or map to gruvbox?
            # User asked for Gruvbox theme. "Cards must follow Gruvbox Dark theme".
            # But for languages, usually people want the official language color.
            # Let's stick to official language colors for the bars, but text in Gruvbox.
            
            bar_width = 200
            fill_width = (percent / 100) * bar_width
            
            bars_svg += f"""
            <g transform="translate(25, {y_offset})">
                <text x="0" y="0" class="stat" style="font-size: 12px;">{html.escape(name)}</text>
                <text x="290" y="0" class="stat" style="font-size: 12px; text-anchor: end;">{percent:.1f}%</text>
                
                <rect x="0" y="8" width="{bar_width}" height="8" rx="4" fill="{self.COLORS['border']}" />
                <rect x="0" y="8" width="{fill_width}" height="8" rx="4" fill="{color}" />
            </g>
            """
            y_offset += 30

        svg = f"""
        <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="{width}" height="{height}" rx="4.5" fill="{self.COLORS['bg']}" stroke="{self.COLORS['border']}" />
            {self._get_style()}
            
            <g transform="translate(25, 35)">
                <text x="0" y="0" class="header">Top Languages</text>
            </g>
            
            {bars_svg}
        </svg>
        """
        return svg
