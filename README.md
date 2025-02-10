# 🎥 AI-Powered YouTube Downloader

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![WCAG 2.1](https://img.shields.io/badge/WCAG-2.1_AA-00A98F?style=for-the-badge)](https://www.w3.org/WAI/WCAG21/quickref/)

A modern, accessible YouTube video downloader built with AI assistance, focusing on user experience and accessibility. Download your favorite videos in high quality while enjoying a clean, intuitive interface that's fully WCAG 2.1 AA compliant.

[Features](#features) • [Quick Start](#quick-start) • [Tech Stack](#tech-stack) • [Development Story](#development-story) • [Deployment](#deployment)

</div>

## 🌟 Features

- **Modern Interface**: Clean, intuitive design with Bootstrap 5
- **Full Accessibility**: WCAG 2.1 AA compliant with screen reader support
- **Real-time Progress**: Live download progress with speed and ETA
- **Format Options**: Best quality MP4 video selection
- **Error Handling**: Robust error management and user feedback
- **High Contrast**: Support for users with visual impairments
- **Keyboard Navigation**: Full keyboard control support

## 🚀 Quick Start

1. **Clone & Install**
```bash
git clone https://github.com/ndweir/ai-youtube-downloader.git
cd ai-youtube-downloader
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run**
```bash
python youtube_downloader.py
```

3. **Use**
```bash
# Start the application
python youtube_downloader.py

# Open in your browser
open http://localhost:5012  # Mac
# or
xdg-open http://localhost:5012  # Linux
# or visit http://localhost:5012 in your browser
```

Then:
1. Paste a YouTube URL
2. Click "Get Video Info"
3. Choose your preferred format
4. Download and enjoy!

## 💻 Tech Stack

<div align="center">
<table>
<tr>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=python" width="48" height="48" alt="Python" />
<br>Python
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=flask" width="48" height="48" alt="Flask" />
<br>Flask
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=js" width="48" height="48" alt="JavaScript" />
<br>JavaScript
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=bootstrap" width="48" height="48" alt="Bootstrap" />
<br>Bootstrap
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=html" width="48" height="48" alt="HTML" />
<br>HTML5
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=css" width="48" height="48" alt="CSS" />
<br>CSS3
</td>
</tr>
</table>
</div>

### Key Components

- **Backend**: Flask server with yt-dlp integration
- **Frontend**: Modern JavaScript with Bootstrap 5
- **Accessibility**: ARIA labels, keyboard navigation, high contrast
- **Development**: Built with AI assistance (Claude & GitHub Copilot)

## 🎯 Development Story

This project showcases my ability to rapidly develop production-ready applications using modern AI tools and best practices. Key highlights:

- **AI-Driven Development**: Used AI assistants to accelerate development while maintaining code quality
- **Accessibility First**: Built with WCAG 2.1 AA compliance from the ground up
- **User-Centric Design**: Focus on intuitive UX and real-time feedback
- **Rapid Iteration**: From concept to production in under 24 hours
- **Best Practices**: Clean code, error handling, and comprehensive documentation

## 🚢 Deployment

### Docker
```bash
docker build -t youtube-downloader .
docker run -p 5012:5012 youtube-downloader
```

### Cloud Platforms

<details>
<summary>Click to expand deployment options</summary>

#### Heroku
```bash
heroku create
git push heroku main
```

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/youtube-downloader
gcloud run deploy --image gcr.io/PROJECT_ID/youtube-downloader
```

</details>

## 📈 Why Choose Me for Your Next Project?

1. **Rapid Development**: Leverage AI tools to accelerate development without compromising quality
2. **Accessibility Expertise**: Deep understanding of WCAG guidelines and implementation
3. **Full Stack Proficiency**: Seamless integration of frontend and backend technologies
4. **User-Centric Focus**: Emphasis on user experience and interface design
5. **Modern Tools**: Experience with latest development practices and technologies

## 🤝 Contributing

Contributions welcome! Please check out our [Contributing Guide](CONTRIBUTING.md).

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

Made with ❤️ and AI by Nick Weir

[Report Bug](https://github.com/ndweir/ai-youtube-downloader/issues) • [Request Feature](https://github.com/ndweir/ai-youtube-downloader/issues)

</div>

```
.
├── app.py              # Main Flask application
├── static/            # Static assets (JS, CSS)
├── templates/         # HTML templates
├── uploads/           # User uploads directory
│   ├── audio/        # Audio files
│   ├── video/        # Video files
│   └── captions/     # Caption files
├── Dockerfile        # Docker configuration
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## License

This project is open source and available under the MIT License.

