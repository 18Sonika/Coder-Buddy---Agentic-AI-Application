import zipfile
import io
from typing import Dict


class ProjectZipper:
    """
    Creates a ZIP archive from generated project files.
    """

    def create_zip(
        self,
        project_name: str,
        files: Dict[str, str]
    ) -> io.BytesIO:
        """
        Create an in-memory ZIP file for the project.

        Returns:
            BytesIO object containing ZIP data.
        """
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename, content in files.items():
                zip_path = f"{project_name}/{filename}"
                zipf.writestr(zip_path, content)

        zip_buffer.seek(0)
        return zip_buffer
