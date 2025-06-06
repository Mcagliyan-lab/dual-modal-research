# Submission-Ready Paper Versions

This directory will contain publication-ready versions of the paper for different venues.

## Planned Submissions

### Primary Target: JMLR
- **Status**: Draft in preparation
- **Timeline**: After NN-fMRI implementation complete
- **Requirements**: Comprehensive methodology + validation

### Secondary Targets
- **NeurIPS**: Focused on methodology innovation; highly competitive, emphasizes novel algorithms.
- **Nature Machine Intelligence**: Emphasizing practical impact; high-impact venue for interdisciplinary AI research.
- **Medical AI venues**: Healthcare applications; target for clinical relevance and specific applications in medical imaging.

## Current Status
- ✅ Theoretical framework complete (See: `theory/nn-fmri-methodology.md`)
- ✅ NN-EEG validated  
- 🟡 NN-fMRI implementation in progress
- ⏳ Integrated validation planned

## Files Will Include
- `jmlr_submission.pdf` - Complete JMLR paper
- `neurips_submission.pdf` - Conference version
- `supplementary_materials.pdf` - Additional details and proofs
- `reproducibility_package.zip` - Code, sample data, and environment setup instructions for full reproducibility

## Update Procedure

To ensure this README.md accurately reflects the paper's submission status and related information, please follow these guidelines:

1.  **Submission Status Changes**:
    *   When the paper is submitted to a new venue, update the `Status` field for that venue under `Planned Submissions`.
    *   Upon acceptance, rejection, or major revisions, update the `Status` and `Timeline` accordingly.
    *   Add new entries for any new planned or actual submissions.

2.  **File Updates**:
    *   As new submission-ready files (e.g., final PDF, supplementary materials, reproducibility package) become available, list them under `Files Will Include`.
    *   Ensure the file names and descriptions are accurate.

3.  **Current Status Section**:
    *   Periodically review and update the `Current Status` checklist to reflect the overall progress of the paper (e.g., NN-fMRI implementation status, integrated validation).

4.  **Responsibility**:
    *   The primary authors or designated documentation maintainers are responsible for keeping this file updated.

5.  **Commit Messages**:
    *   When updating this file, use clear and descriptive commit messages that indicate the nature of the status change (e.g., "Update: JMLR submission status to 'Under Review'", "Add: NeurIPS submission entry"). 

## Version Control and Archiving

- **Version Naming:** For multiple revisions of a paper, use clear version naming conventions (e.g., `paper_v1.0.pdf`, `paper_v1.1_minor_revisions.pdf`).
- **Archiving:** Old or rejected versions of papers and supplementary materials should be moved to an `archive` subdirectory within this directory to maintain a clean working space while preserving history. 