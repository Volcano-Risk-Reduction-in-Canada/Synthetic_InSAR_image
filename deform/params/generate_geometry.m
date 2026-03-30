function [Heading, Incidence] = generate_geometry()
    % [ascending_headings, descending_headings]
    heading_choices = [65:2:95, 175:2:205];
    Heading = heading_choices(randi(length(heading_choices)));

    incidence_choices = 19:2:51;
    Incidence = incidence_choices(randi(length(incidence_choices)));

end

