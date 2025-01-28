# import pytest
# from unittest.mock import Mock
# from lease_entry.services.lease_detail_extractor import LeaseDetailExtractor
# from lease_entry.types.lease_detail import LeaseDetail

# class MockLeaseEntry:
#     def __init__(self, entry_text):
#         self.entryText = entry_text

# class TestLeaseDetailExtractor:
#     @pytest.fixture
#     def mock_repository(self):
#         return Mock()

#     @pytest.fixture
#     def extractor(self, mock_repository):
#         return LeaseDetailExtractor(mock_repository)

#     def test_transformer_chamber_extraction(self, extractor, mock_repository):
#         # Arrange
#         entry_text = [
#             "28.01.2009      Transformer Chamber (Ground   23.01.2009      EGL551039  ",
#             "tinted blue     Floor)                        99 years from              ",
#             "(part of)                                     23.1.2009"
#         ]
#         mock_repository.get.return_value = MockLeaseEntry(entry_text)

#         # Act
#         result = extractor.extract_lease_detail("1")

#         # Assert
#         assert isinstance(result, LeaseDetail)
#         assert result.registration_date_and_plan_ref == "28.01.2009 tinted blue (part of)"
#         assert result.property_description == "Transformer Chamber (Ground Floor)"
#         assert result.date_of_lease_and_term == "23.01.2009 99 years from 23.1.2009"
#         assert result.lessee_title == "EGL551039"
#         assert result.note_1 is None

#     def test_endeavour_house_extraction(self, extractor, mock_repository):
#         # Arrange
#         entry_text = [
#             "09.07.2009      Endeavour House, 47 Cuba      06.07.2009      EGL557357  ",
#             "Edged and       Street, London                125 years from             ",
#             "numbered 2 in                                 1.1.2009                   ",
#             "blue (part of)"
#         ]
#         mock_repository.get.return_value = MockLeaseEntry(entry_text)

#         # Act
#         result = extractor.extract_lease_detail("2")

#         # Assert
#         assert isinstance(result, LeaseDetail)
#         assert result.registration_date_and_plan_ref == "09.07.2009 Edged and numbered 2 in blue (part of)"
#         assert result.property_description == "Endeavour House, 47 Cuba Street, London"
#         assert result.date_of_lease_and_term == "06.07.2009 125 years from 1.1.2009"
#         assert result.lessee_title == "EGL557357"
#         assert result.note_1 is None

#     def test_flat_extraction(self, extractor, mock_repository):
#         # Arrange
#         entry_text = [
#             "16.12.2009      Flat 1602, Landmark West      12.11.2009      EGL565026  ",
#             "Edged and       Tower(sixteenth floor)        999 years from             ",
#             "numbered 4 in                                 1.1.2009                   ",
#             "blue (part of)"
#         ]
#         mock_repository.get.return_value = MockLeaseEntry(entry_text)

#         # Act
#         result = extractor.extract_lease_detail("4")

#         # Assert
#         assert isinstance(result, LeaseDetail)
#         assert result.registration_date_and_plan_ref == "16.12.2009 Edged and numbered 4 in blue (part of)"
#         assert result.property_description == "Flat 1602, Landmark West Tower(sixteenth floor)"
#         assert result.date_of_lease_and_term == "12.11.2009 999 years from 1.1.2009"
#         assert result.lessee_title == "EGL565026"
#         assert result.note_1 is None

#     def test_extraction_with_note(self, extractor, mock_repository):
#         # Arrange
#         entry_text = [
#             "31.10.2016      Retail Warehouse, The         25.07.1996      SY664660  ",
#             "1 in yellow     Causeway and River Park       25 years from             ",
#             "                Avenue, Staines               25.3.1995                  ",
#             "NOTE: The Lease comprises also other land"
#         ]
#         mock_repository.get.return_value = MockLeaseEntry(entry_text)

#         # Act
#         result = extractor.extract_lease_detail("test")

#         # Assert
#         assert isinstance(result, LeaseDetail)
#         assert result.registration_date_and_plan_ref == "31.10.2016 1 in yellow"
#         assert result.property_description == "Retail Warehouse, The Causeway and River Park Avenue, Staines"
#         assert result.date_of_lease_and_term == "25.07.1996 25 years from 25.3.1995"
#         assert result.lessee_title == "SY664660"
#         assert result.note_1 == "NOTE: The Lease comprises also other land"

#     def test_extract_lessee_title(self, extractor):
#         # Test successful extraction
#         lines = ["Some text AGL123456 more text"]
#         lessee_title, remaining_lines = extractor.extract_lessee_title(lines)
#         assert lessee_title == "AGL123456"
#         assert remaining_lines[0] == "Some text more text"

#         # Test no lessee title
#         lines = ["Some text without lessee title"]
#         lessee_title, remaining_lines = extractor.extract_lessee_title(lines)
#         assert lessee_title is None
#         assert remaining_lines[0] == "Some text without lessee title"

#     def test_extract_dates(self, extractor):
#         # Test date extraction
#         lines = ["Text with dates 01.02.2023 and 03.04.2023"]
        
#         # Test date of lease extraction
#         date_of_lease, lines = extractor.extract_date_of_lease(lines)
#         assert date_of_lease == "03.04.2023"
        
#         # Test registration date extraction
#         registration_date, lines = extractor.extract_registration_date(lines)
#         assert registration_date == "01.02.2023"

#     def test_extract_term(self, extractor):
#         lines = [
#             "First line",
#             "Term is 99 years from",
#             "starting 01.01.2020 text",
#         ]
#         term, remaining_lines = extractor.extract_term(lines)
#         assert term == "99 years from 01.01.2020"
#         assert remaining_lines[1] == "Term is"
#         assert remaining_lines[2] == "starting text"

#     def test_extract_note(self, extractor):
#         # Test with note
#         lines = ["Some text", "More text", "NOTE: This is a note"]
#         note, remaining_lines = extractor.extract_note(lines)
#         assert note == "NOTE: This is a note"
#         assert len(remaining_lines) == 2

#         # Test without note
#         lines = ["Some text", "More text", "Not a note"]
#         note, remaining_lines = extractor.extract_note(lines)
#         assert note is None
#         assert len(remaining_lines) == 3

#     def test_extract_lease_detail_integration(self, extractor, mock_repository):
#         # Mock the repository response
#         mock_entry = Mock()
#         mock_entry.entryText = [
#             "Property details AGL123456 01.02.2023 03.04.2023",
#             "Term is 99 years from",
#             "starting 01.01.2020 text",
#             "Edged and numbered 123 in blue on",
#             "plan 1",
#             "Some property description",
#             "NOTE: Important note"
#         ]
#         mock_repository.get.return_value = mock_entry

#         # Test the full extraction
#         result = extractor.extract_lease_detail("ENTRY123")

#         assert isinstance(result, LeaseDetail)
#         assert result.lessee_title == "AGL123456"
#         assert "99 years from 01.01.2020" in result.date_of_lease_and_term
#         assert "03.04.2023" in result.date_of_lease_and_term
#         assert "01.02.2023" in result.registration_date_and_plan_ref
#         assert "Edged and numbered 123 in blue on plan 1" in result.registration_date_and_plan_ref
#         assert result.note_1 == "NOTE: Important note"
#         assert "Some property description" in result.property_description 