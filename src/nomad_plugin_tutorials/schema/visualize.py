import numpy as np
import plotly.graph_objs as go


def plot_blackbody_spectrum(
    temperature: float,
    wavelength: list[float],
    spectral_radiance: list[float],
    peak_wavelength: float | None = None,
) -> go.Figure:
    """
    Creates a Plotly line plot of the Planck spectral radiance B(λ, T).
    Radiance is normalised to 1 for readability. An optional dashed vertical
    line marks the Wien peak wavelength.

    Args:
        temperature:      Temperature of the blackbody in Kelvin (used for plot title).
        wavelength:        Wavelength array in nm.
        spectral_radiance: B(λ, T) values (any units; will be normalised).
        peak_wavelength:   λ_max in nm from Wien's law (optional).

    Returns:
        go.Figure
    """
    radiance_norm = np.array(spectral_radiance)
    radiance_norm = radiance_norm / radiance_norm.max()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(wavelength),
            y=radiance_norm.tolist(),
            mode='lines',
            name='B(λ, T)',
            line=dict(color='steelblue', width=2),
            fill='tozeroy',
            fillcolor='rgba(70,130,180,0.15)',
        )
    )
    if peak_wavelength is not None:
        fig.add_vline(
            x=peak_wavelength,
            line=dict(color='firebrick', width=1, dash='dash'),
            annotation_text=f'λ_max = {peak_wavelength:.0f} nm',
            annotation_position='top right',
        )
    fig.update_layout(
        title=f'Planck Spectral Radiance B(λ, T) at {temperature:.0f} K',
        xaxis_title='Wavelength (nm)',
        yaxis_title='Normalised Spectral Radiance',
        template='plotly_white',
        xaxis=dict(fixedrange=False),
        yaxis=dict(fixedrange=False),
    )
    return fig
