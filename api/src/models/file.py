from dataclasses import dataclass

from github.ContentFile import ContentFile

@dataclass(frozen=True)
class ContentFileData:
    path: str
    name: str
    html_url: str
    sha: str
    download_url: str
    content: str
    repository_name: str
    language: str
    type: str

    def from_content_file(file: ContentFile):
        try:
            content = file.decoded_content.decode('utf-8')
        except:
            content = ""

        return ContentFileData(
            file.path,
            file.name,
            file.html_url,
            file.sha,
            file.download_url,
            content,
            file.repository.name,
            file.language,
            file.type
        )
    









