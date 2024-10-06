class Settings:
    allow_indexed: bool
    allow_mounted: bool
    announcement: str
    audio_autoplay: bool
    audio_cover: str
    auto_update_index: bool
    default_page_size: int
    external_previews: str
    favicon: str
    filename_char_mapping: str
    forward_direct_link_params: bool
    hide_files: str
    home_container: str
    home_icon: str
    iframe_previews: str
    ignore_direct_link_params: str
    ldap_login_enabled: bool
    ldap_login_tips: str
    logo: str
    main_color: str
    ocr_api: str
    package_download: bool
    pagination_type: str
    robots_txt: str
    search_index: str
    settings_layout: str
    site_title: str
    sso_compatibility_mode: bool
    sso_login_enabled: bool
    sso_login_platform: str
    version: str
    video_autoplay: bool
    webauthn_login_enabled: bool

    def __init__(self, allow_indexed: bool, allow_mounted: bool, announcement: str, audio_autoplay: bool, audio_cover: str, auto_update_index: bool, default_page_size: int, external_previews: str, favicon: str, filename_char_mapping: str, forward_direct_link_params: bool, hide_files: str, home_container: str, home_icon: str, iframe_previews: str, ignore_direct_link_params: str, ldap_login_enabled: bool, ldap_login_tips: str, logo: str, main_color: str, ocr_api: str, package_download: bool, pagination_type: str, robots_txt: str, search_index: str, settings_layout: str, site_title: str, sso_compatibility_mode: bool, sso_login_enabled: bool, sso_login_platform: str, version: str, video_autoplay: bool, webauthn_login_enabled: bool) -> None:
        self.allow_indexed = allow_indexed
        self.allow_mounted = allow_mounted
        self.announcement = announcement
        self.audio_autoplay = audio_autoplay
        self.audio_cover = audio_cover
        self.auto_update_index = auto_update_index
        self.default_page_size = default_page_size
        self.external_previews = external_previews
        self.favicon = favicon
        self.filename_char_mapping = filename_char_mapping
        self.forward_direct_link_params = forward_direct_link_params
        self.hide_files = hide_files
        self.home_container = home_container
        self.home_icon = home_icon
        self.iframe_previews = iframe_previews
        self.ignore_direct_link_params = ignore_direct_link_params
        self.ldap_login_enabled = ldap_login_enabled
        self.ldap_login_tips = ldap_login_tips
        self.logo = logo
        self.main_color = main_color
        self.ocr_api = ocr_api
        self.package_download = package_download
        self.pagination_type = pagination_type
        self.robots_txt = robots_txt
        self.search_index = search_index
        self.settings_layout = settings_layout
        self.site_title = site_title
        self.sso_compatibility_mode = sso_compatibility_mode
        self.sso_login_enabled = sso_login_enabled
        self.sso_login_platform = sso_login_platform
        self.version = version
        self.video_autoplay = video_autoplay
        self.webauthn_login_enabled = webauthn_login_enabled